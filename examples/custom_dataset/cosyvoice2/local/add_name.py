import os
import argparse
from pathlib import Path

def process_normalized_files(directory, prefix="MarchSeventh"):
    """
    遍历指定目录下的.normalized.txt文件，检查是否有对应的.wav文件
    如果有对应的wav文件，则在txt文件开头添加指定前缀
    如果没有对应的wav文件，则删除该txt文件
    
    Args:
        directory: 目标目录路径
        prefix: 要添加的前缀文本（不包含<|endofprompt|>）
    """
    directory_path = Path(directory)
    
    # 检查目录是否存在
    if not directory_path.exists():
        print(f"错误: 目录 {directory} 不存在！")
        return
    
    # 遍历所有.normalized.txt文件
    normalized_files = list(directory_path.glob("*.normalized.txt"))
    
    if not normalized_files:
        print(f"在目录 {directory} 中未找到.normalized.txt文件")
        return
    
    print(f"找到 {len(normalized_files)} 个.normalized.txt文件")
    print(f"使用前缀: {prefix}<|endofprompt|>\n")
    
    processed_count = 0
    deleted_count = 0
    
    for txt_file in normalized_files:
        # 获取基础文件名（去掉.normalized.txt后缀）
        base_name = txt_file.name.replace('.normalized.txt', '')
        
        # 构建对应的wav文件路径
        wav_file = directory_path / f"{base_name}.wav"
        
        if wav_file.exists():
            # 如果wav文件存在，读取txt内容并添加前缀
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 构建完整前缀
                full_prefix = f"{prefix}<|endofprompt|>"
                
                # 检查是否已经添加过前缀（避免重复添加）
                if not content.startswith(full_prefix):
                    new_content = full_prefix + content
                    
                    with open(txt_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"✓ 已处理: {txt_file.name}")
                    processed_count += 1
                else:
                    print(f"⊙ 跳过（已有前缀）: {txt_file.name}")
                    
            except Exception as e:
                print(f"✗ 处理失败 {txt_file.name}: {e}")
        else:
            # 如果wav文件不存在，删除txt文件
            try:
                txt_file.unlink()
                print(f"✗ 已删除（无对应wav）: {txt_file.name}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ 删除失败 {txt_file.name}: {e}")
    
    print(f"\n处理完成！")
    print(f"成功处理: {processed_count} 个文件")
    print(f"删除文件: {deleted_count} 个文件")

def main():
    parser = argparse.ArgumentParser(
        description='处理.normalized.txt文件：添加前缀或删除无对应wav的文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s -d /path/to/directory
  %(prog)s -d /path/to/directory -p "CustomPrefix"
  %(prog)s --directory "D:\\Data\\Audio" --prefix "MyCharacter"
        """)
    
    parser.add_argument('-d', '--directory',
                        type=str,
                        required=True,
                        help='指定要处理的目录路径')
    
    parser.add_argument('-p', '--prefix',
                        type=str,
                        default='CustomCharacter',
                        help='指定要添加的前缀（默认: MarchSeventh）')
    
    args = parser.parse_args()
    
    process_normalized_files(args.directory, args.prefix)

if __name__ == "__main__":
    main()
