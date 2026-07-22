import sys
import argparse
from orchestrator.replay import ReplayEngine

def main():
    parser = argparse.ArgumentParser(description="Replay and debug AutoGen workflow runs.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all available runs.")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show the chat transcript for a run.")
    show_parser.add_argument("run_id", help="The UUID of the run to display.")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract generated files to a directory.")
    extract_parser.add_argument("run_id", help="The UUID of the run.")
    extract_parser.add_argument("target_dir", help="Directory to extract the files to.")

    args = parser.parse_args()
    engine = ReplayEngine()
    
    if args.command == "list":
        runs = engine.list_runs()
        if not runs:
            print("No runs found in artifacts/")
        else:
            print(f"{'Run ID':<40} {'Date'}")
            print("-" * 60)
            for run in runs:
                print(f"{run['run_id']:<40} {run['date']}")
                
    elif args.command == "show":
        try:
            engine.print_transcript(args.run_id)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            
    elif args.command == "extract":
        try:
            engine.export_files(args.run_id, args.target_dir)
        except FileNotFoundError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
