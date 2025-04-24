from visualizer import plot_market_regime_to_html
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("❗Usage: python main.py <path_to_excel_file>")
        return

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"❗File not found: {file_path}")
        return

    plot_market_regime_to_html(file_path)

if __name__ == "__main__":
    main()
