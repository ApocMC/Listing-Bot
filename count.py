import os
import glob
from pathlib import Path

def count_lines_in_file(file_path):
    """Count total lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

def count_python_files(directory, exclude_dirs=['venv', '__pycache__', '.git', 'node_modules']):
    """Count lines in Python files, excluding specified directories."""
    total_lines = 0
    file_count = 0
    files_info = []
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                lines = count_lines_in_file(file_path)
                total_lines += lines
                file_count += 1
                files_info.append((file_path, lines))
    
    return total_lines, file_count, files_info

def count_js_files_in_src(directory):
    """Count lines in JavaScript files within src/ directory."""
    total_lines = 0
    file_count = 0
    files_info = []
    
    src_path = os.path.join(directory, 'src')
    if not os.path.exists(src_path):
        return 0, 0, []
    
    for root, dirs, files in os.walk(src_path):
        # Exclude node_modules and other build directories
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist', 'build']]
        
        for file in files:
            if file.endswith('.js') or file.endswith('.jsx') or file.endswith('.ts') or file.endswith('.tsx'):
                file_path = os.path.join(root, file)
                lines = count_lines_in_file(file_path)
                total_lines += lines
                file_count += 1
                files_info.append((file_path, lines))
    
    return total_lines, file_count, files_info

def count_api_py(directory):
    """Count lines in api.py file."""
    api_path = os.path.join(directory, 'api.py')
    if os.path.exists(api_path):
        lines = count_lines_in_file(api_path)
        return lines, 1, [(api_path, lines)]
    return 0, 0, []

def print_project_stats(project_name, total_lines, file_count, files_info, base_path=""):
    """Print formatted statistics for a project."""
    print(f"\n{'='*60}")
    print(f"📊 {project_name}")
    print(f"{'='*60}")
    print(f"📁 Total Files: {file_count}")
    print(f"📝 Total Lines: {total_lines:,}")
    print(f"📈 Average Lines per File: {total_lines/file_count if file_count > 0 else 0:.1f}")
    
    if files_info:
        print(f"\n📋 File Breakdown:")
        sorted_files = sorted(files_info, key=lambda x: x[1], reverse=True)
        
        for file_path, lines in sorted_files:
            if base_path:
                try:
                    rel_path = os.path.relpath(file_path, base_path)
                except ValueError:
                    rel_path = file_path
            else:
                rel_path = file_path
            
            print(f"  📄 {rel_path:<50} {lines:>6,} lines")

def main():
    base_dir = "./"
    
    projects = [
        ("Listing Bot", os.path.join(base_dir, "listing-bot"), "python"),
        ("Listing Bot Dashboard", os.path.join(base_dir, "listing-bot-dashboard"), "javascript"),
        ("Seller Dashboard", os.path.join(base_dir, "seller_dashboard"), "javascript"),
        ("Parent API", os.path.join(base_dir, "parent_api"), "api"),
        ("Shop Websites", os.path.join(base_dir, "shop-sites"), "javascript"),
    ]
    
    total_all_lines = 0
    total_all_files = 0
    
    print("🚀 CODE STATISTICS REPORT")
    print(f"Generated on: {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}")
    
    for project_name, project_path, project_type in projects:
        if not os.path.exists(project_path):
            print(f"\n⚠️  Warning: {project_name} directory not found at {project_path}")
            continue
        
        if project_type == "python":
            total_lines, file_count, files_info = count_python_files(project_path)
        elif project_type == "javascript":
            total_lines, file_count, files_info = count_js_files_in_src(project_path)
        elif project_type == "api":
            total_lines, file_count, files_info = count_api_py(project_path)
        
        print_project_stats(project_name, total_lines, file_count, files_info, project_path)
        
        total_all_lines += total_lines
        total_all_files += file_count
    
    print(f"\n{'='*60}")
    print(f"🎯 OVERALL SUMMARY")
    print(f"{'='*60}")
    print(f"🔢 Total Projects: {len([p for p in projects if os.path.exists(p[1])])}")
    print(f"📁 Total Files: {total_all_files}")
    print(f"📝 Total Lines of Code: {total_all_lines:,}")
    print(f"📊 Average Lines per Project: {total_all_lines/len([p for p in projects if os.path.exists(p[1])]) if len([p for p in projects if os.path.exists(p[1])]) > 0 else 0:.1f}")
    
    print(f"\n🎉 Analysis Complete!")

if __name__ == "__main__":
    main()