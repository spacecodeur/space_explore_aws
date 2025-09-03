#!/usr/bin/env python3
import json
import sys
import os
import subprocess
from pathlib import Path


class CommandManager:
    def __init__(self, commands_dir="commands"):
        self.commands_dir = Path(commands_dir)
        self.commands = {}
        self.load_commands()
    
    def load_commands(self):
        """Charge toutes les commandes depuis les fichiers JSON"""
        if not self.commands_dir.exists():
            self.commands_dir.mkdir(exist_ok=True)
            return
        
        for json_file in self.commands_dir.rglob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    command_data = json.load(f)
                    # Utiliser le chemin relatif comme clé
                    relative_path = json_file.relative_to(self.commands_dir.parent)
                    self.commands[str(relative_path)] = command_data
            except Exception as e:
                print(f"Erreur lors du chargement de {json_file}: {e}")
    
    def list_commands(self):
        """Liste toutes les commandes disponibles"""
        if not self.commands:
            print("Aucune commande disponible.")
            return
        
        print("Commandes disponibles:")
        print("=" * 50)
        for name, data in self.commands.items():
            print(f"• {name}: {data.get('description', 'Pas de description')}")
        print("\nUtilisez 'chemin/vers/commande.json -h' pour voir l'aide détaillée")
    
    def show_help(self, command_name):
        """Affiche l'aide détaillée pour une commande"""
        if command_name not in self.commands:
            print(f"Commande '{command_name}' introuvable.")
            return
        
        cmd = self.commands[command_name]
        
        print(f"\nCommande: {command_name}")
        print("=" * (len(command_name) + 10))
        print(f"Description: {cmd.get('description', 'Pas de description')}")
        
        if 'parameters' in cmd and cmd['parameters']:
            print("\nParamètres:")
            for i, param in enumerate(cmd['parameters'], 1):
                print(f"  ${i} - {param['name']}: {param['description']}")
        
        if 'example' in cmd:
            print(f"\nExemple d'utilisation:")
            print(f"  {cmd['example']}")
        
        if 'command' in cmd:
            print(f"\nCommande technique exécutée:")
            print(f"  {cmd['command']}")
    
    def execute_command(self, command_name, args):
        """Exécute une commande avec les arguments fournis"""
        if command_name not in self.commands:
            print(f"Commande '{command_name}' introuvable.")
            return
        
        cmd = self.commands[command_name]
        required_params = len(cmd.get('parameters', []))
        
        if len(args) != required_params:
            print(f"Erreur: {required_params} paramètre(s) requis, {len(args)} fourni(s)")
            self.show_help(command_name)
            return
        
        # Substitution des variables $1, $2, etc.
        command_to_execute = cmd['command']
        for i, arg in enumerate(args, 1):
            command_to_execute = command_to_execute.replace(f"${i}", arg)
        
        print(f"Exécution: {command_to_execute}")
        
        try:
            # Pour les commandes interactives (ssh, nano, vim, etc.), 
            # ne pas capturer les flux pour permettre l'interaction
            interactive_commands = ['ssh', 'nano', 'vim', 'vi', 'emacs', 'less', 'more', 'htop', 'top']
            first_word = command_to_execute.strip().split()[0].lower() if command_to_execute.strip() else ""
            is_interactive = first_word in interactive_commands
            
            if is_interactive:
                # Exécution interactive - pas de capture des flux
                result = subprocess.run(command_to_execute, shell=True)
                return result.returncode
            else:
                # Exécution normale avec capture des flux
                result = subprocess.run(command_to_execute, shell=True, 
                                      capture_output=True, text=True)
                
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(f"Erreur: {result.stderr}")
                
                return result.returncode
        except Exception as e:
            print(f"Erreur lors de l'exécution: {e}")
            return 1
    
    def load_single_command(self, json_file_path):
        """Charge une seule commande depuis un fichier JSON"""
        try:
            json_path = Path(json_file_path)
            if not json_path.exists():
                print(f"Fichier '{json_file_path}' introuvable.")
                return None
            
            with open(json_path, 'r', encoding='utf-8') as f:
                command_data = json.load(f)
                return command_data
        except Exception as e:
            print(f"Erreur lors du chargement de {json_file_path}: {e}")
            return None
    
    def execute_single_command(self, json_file_path, args):
        """Exécute une commande directement depuis un fichier JSON"""
        cmd = self.load_single_command(json_file_path)
        if not cmd:
            return
        
        # Vérifier si c'est une demande d'aide
        if len(args) == 1 and args[0] == "-h":
            command_name = Path(json_file_path).stem
            print(f"\nCommande: {command_name}")
            print("=" * (len(command_name) + 10))
            print(f"Description: {cmd.get('description', 'Pas de description')}")
            
            if 'parameters' in cmd and cmd['parameters']:
                print("\nParamètres:")
                for i, param in enumerate(cmd['parameters'], 1):
                    print(f"  ${i} - {param['name']}: {param['description']}")
            
            if 'example' in cmd:
                print(f"\nExemple d'utilisation:")
                print(f"  {cmd['example']}")
            
            if 'command' in cmd:
                print(f"\nCommande technique exécutée:")
                print(f"  {cmd['command']}")
            return
        
        required_params = len(cmd.get('parameters', []))
        
        if len(args) != required_params:
            print(f"Erreur: {required_params} paramètre(s) requis, {len(args)} fourni(s)")
            # Afficher l'aide automatiquement
            self.execute_single_command(json_file_path, ["-h"])
            return
        
        # Substitution des variables $1, $2, etc.
        command_to_execute = cmd['command']
        for i, arg in enumerate(args, 1):
            command_to_execute = command_to_execute.replace(f"${i}", arg)
        
        print(f"Exécution: {command_to_execute}")
        
        try:
            # Pour les commandes interactives (ssh, nano, vim, etc.), 
            # ne pas capturer les flux pour permettre l'interaction
            interactive_commands = ['ssh', 'nano', 'vim', 'vi', 'emacs', 'less', 'more', 'htop', 'top']
            first_word = command_to_execute.strip().split()[0].lower() if command_to_execute.strip() else ""
            is_interactive = first_word in interactive_commands
            
            if is_interactive:
                # Exécution interactive - pas de capture des flux
                result = subprocess.run(command_to_execute, shell=True)
                return result.returncode
            else:
                # Exécution normale avec capture des flux
                result = subprocess.run(command_to_execute, shell=True, 
                                      capture_output=True, text=True)
                
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(f"Erreur: {result.stderr}")
                
                return result.returncode
        except Exception as e:
            print(f"Erreur lors de l'exécution: {e}")
            return 1

    def run(self, args):
        """Point d'entrée principal"""
        if not args:
            self.list_commands()
            return
        
        first_arg = args[0]
        
        # Vérifier si le premier argument est un chemin vers un fichier JSON
        if first_arg.endswith('.json') and ('/' in first_arg or '\\' in first_arg):
            # Mode fichier direct
            self.execute_single_command(first_arg, args[1:])
            return
        
        # Mode commande par nom (ancien comportement)
        command_name = first_arg
        
        # Vérifier si c'est une demande d'aide
        if len(args) == 2 and args[1] == "-h":
            self.show_help(command_name)
            return
        
        # Exécuter la commande
        self.execute_command(command_name, args[1:])


def main():
    manager = CommandManager()
    manager.run(sys.argv[1:])


if __name__ == "__main__":
    main()