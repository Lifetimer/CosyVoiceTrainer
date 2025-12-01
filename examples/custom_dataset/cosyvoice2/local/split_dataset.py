import os
import random
import argparse
from shutil import move

def split_dataset(data_dir, output_dir, train_ratio=0.8):
    """
    将数据集按照指定比例分为训练集和测试集
    
    参数:
        data_dir: 数据集目录路径
        output_dir: 输出目录路径
        train_ratio: 训练集比例，默认0.8
    """
    
    # 创建输出目录
    train_dir = os.path.join(output_dir, 'train_dataset')
    test_dir = os.path.join(output_dir, 'test_dataset')
    
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    # 获取所有.normalized.txt文件
    all_files = os.listdir(data_dir)
    txt_files = [f for f in all_files if f.endswith('.normalized.txt')]
    
    # 提取基础名字（去掉.normalized.txt后缀）
    base_names = [f.replace('.normalized.txt', '') for f in txt_files]
    
    # 验证每个txt文件都有对应的wav文件
    valid_pairs = []
    for name in base_names:
        txt_file = f"{name}.normalized.txt"
        wav_file = f"{name}.wav"
        
        if os.path.exists(os.path.join(data_dir, txt_file)) and \
           os.path.exists(os.path.join(data_dir, wav_file)):
            valid_pairs.append(name)
        else:
            print(f"警告: {name} 缺少配对文件，已跳过")
    
    # 打乱顺序
    random.shuffle(valid_pairs)
    
    # 计算分割点
    split_idx = int(len(valid_pairs) * train_ratio)
    train_pairs = valid_pairs[:split_idx]
    test_pairs = valid_pairs[split_idx:]
    
    # 移动文件到训练集
    print(f"移动训练集文件 ({len(train_pairs)} 对)...")
    for name in train_pairs:
        txt_file = f"{name}.normalized.txt"
        wav_file = f"{name}.wav"
        
        move(os.path.join(data_dir, txt_file), os.path.join(train_dir, txt_file))
        move(os.path.join(data_dir, wav_file), os.path.join(train_dir, wav_file))
    
    # 移动文件到测试集
    print(f"移动测试集文件 ({len(test_pairs)} 对)...")
    for name in test_pairs:
        txt_file = f"{name}.normalized.txt"
        wav_file = f"{name}.wav"
        
        move(os.path.join(data_dir, txt_file), os.path.join(test_dir, txt_file))
        move(os.path.join(data_dir, wav_file), os.path.join(test_dir, wav_file))
    
    # 输出统计信息
    print("\n数据集分割完成！")
    print(f"总数据对数: {len(valid_pairs)}")
    print(f"训练集: {len(train_pairs)} 对 ({len(train_pairs)/len(valid_pairs)*100:.1f}%)")
    print(f"测试集: {len(test_pairs)} 对 ({len(test_pairs)/len(valid_pairs)*100:.1f}%)")
    print(f"\n训练集目录: {train_dir}")
    print(f"测试集目录: {test_dir}")

def main():
    parser = argparse.ArgumentParser(
        description='将数据集按照指定比例分为训练集和测试集',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s -i /path/to/dataset -o /path/to/output -r 0.8
  %(prog)s --input-dir ./data --output-dir ./split_data --ratio 0.9
  %(prog)s -i ./data  # 使用输入目录作为输出目录，默认比例0.8
        '''
    )
    
    parser.add_argument(
        '-i', '--input-dir',
        type=str,
        required=True,
        help='输入数据集目录路径'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default=None,
        help='输出目录路径（默认为输入目录）'
    )
    
    parser.add_argument(
        '-r', '--ratio',
        type=float,
        default=0.8,
        help='训练集比例，范围0-1（默认: 0.8）'
    )
    
    parser.add_argument(
        '-s', '--seed',
        type=int,
        default=42,
        help='随机种子，用于结果复现（默认: 42）'
    )
    
    args = parser.parse_args()
    
    # 验证输入目录是否存在
    if not os.path.exists(args.input_dir):
        parser.error(f"输入目录不存在: {args.input_dir}")
    
    # 验证比例范围
    if not 0 < args.ratio < 1:
        parser.error(f"训练集比例必须在0-1之间，当前值: {args.ratio}")
    
    # 如果未指定输出目录，使用输入目录
    output_dir = args.output_dir if args.output_dir else args.input_dir
    
    # 设置随机种子
    random.seed(args.seed)
    
    # 执行分割
    print(f"输入目录: {args.input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"训练集比例: {args.ratio}")
    print(f"随机种子: {args.seed}")
    print("-" * 50)
    
    split_dataset(args.input_dir, output_dir, args.ratio)

if __name__ == "__main__":
    main()
