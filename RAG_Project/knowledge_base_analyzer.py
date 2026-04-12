"""
知识库分析工具
用于分析知识库的使用情况和统计信息
"""
import os
import json
import datetime
from collections import Counter
from knowledge_base import KnowledgeBaseService
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config


class KnowledgeBaseAnalyzer:
    def __init__(self):
        self.knowledge_base = KnowledgeBaseService()
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )
    
    def get_document_count(self):
        """获取知识库中的文档数量"""
        try:
            # 获取所有文档
            documents = self.vector_service.vector_store.get()
            return len(documents.get('documents', []))
        except Exception as e:
            print(f"获取文档数量失败: {str(e)}")
            return 0
    
    def get_unique_sources(self):
        """获取唯一的文档来源"""
        try:
            documents = self.vector_service.vector_store.get()
            metadatas = documents.get('metadatas', [])
            sources = [meta.get('source', 'unknown') for meta in metadatas]
            unique_sources = list(set(sources))
            return unique_sources
        except Exception as e:
            print(f"获取唯一来源失败: {str(e)}")
            return []
    
    def get_source_statistics(self):
        """获取各来源的文档数量统计"""
        try:
            documents = self.vector_service.vector_store.get()
            metadatas = documents.get('metadatas', [])
            sources = [meta.get('source', 'unknown') for meta in metadatas]
            source_counter = Counter(sources)
            return dict(source_counter)
        except Exception as e:
            print(f"获取来源统计失败: {str(e)}")
            return {}
    
    def get_creation_time_statistics(self):
        """获取文档创建时间统计"""
        try:
            documents = self.vector_service.vector_store.get()
            metadatas = documents.get('metadatas', [])
            creation_times = [meta.get('create_time', '') for meta in metadatas]
            
            # 按日期统计
            date_counter = Counter()
            for time_str in creation_times:
                if time_str:
                    date = time_str.split(' ')[0]  # 提取日期部分
                    date_counter[date] += 1
            
            return dict(date_counter)
        except Exception as e:
            print(f"获取创建时间统计失败: {str(e)}")
            return {}
    
    def analyze_document_length(self):
        """分析文档长度分布"""
        try:
            documents = self.vector_service.vector_store.get()
            document_texts = documents.get('documents', [])
            lengths = [len(doc) for doc in document_texts]
            
            if lengths:
                return {
                    'average_length': sum(lengths) / len(lengths),
                    'min_length': min(lengths),
                    'max_length': max(lengths),
                    'total_length': sum(lengths)
                }
            else:
                return {
                    'average_length': 0,
                    'min_length': 0,
                    'max_length': 0,
                    'total_length': 0
                }
        except Exception as e:
            print(f"分析文档长度失败: {str(e)}")
            return {
                'average_length': 0,
                'min_length': 0,
                'max_length': 0,
                'total_length': 0
            }
    
    def generate_analysis_report(self):
        """生成完整的分析报告"""
        report = {
            'report_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'document_count': self.get_document_count(),
            'unique_sources': self.get_unique_sources(),
            'source_statistics': self.get_source_statistics(),
            'creation_time_statistics': self.get_creation_time_statistics(),
            'document_length_analysis': self.analyze_document_length(),
            'config': {
                'chunk_size': config.chunk_size,
                'chunk_overlap': config.chunk_overlap,
                'similarity_threshold': config.similarity_threshold
            }
        }
        
        # 保存报告到文件
        report_file = f"knowledge_base_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report, report_file
    
    def display_analysis(self):
        """显示分析结果"""
        report, report_file = self.generate_analysis_report()
        
        print("知识库分析报告")
        print("=" * 50)
        print(f"报告生成时间: {report['report_time']}")
        print(f"文档总数: {report['document_count']}")
        print(f"唯一来源数量: {len(report['unique_sources'])}")
        print(f"来源列表: {report['unique_sources']}")
        print("\n各来源文档数量:")
        for source, count in report['source_statistics'].items():
            print(f"  {source}: {count}")
        print("\n按日期创建统计:")
        for date, count in report['creation_time_statistics'].items():
            print(f"  {date}: {count}")
        print("\n文档长度分析:")
        print(f"  平均长度: {report['document_length_analysis']['average_length']:.2f} 字符")
        print(f"  最小长度: {report['document_length_analysis']['min_length']} 字符")
        print(f"  最大长度: {report['document_length_analysis']['max_length']} 字符")
        print(f"  总长度: {report['document_length_analysis']['total_length']} 字符")
        print("\n系统配置:")
        print(f"  Chunk Size: {report['config']['chunk_size']}")
        print(f"  Chunk Overlap: {report['config']['chunk_overlap']}")
        print(f"  Similarity Threshold: {report['config']['similarity_threshold']}")
        print("\n" + "=" * 50)
        print(f"报告已保存到: {report_file}")


if __name__ == '__main__':
    analyzer = KnowledgeBaseAnalyzer()
    analyzer.display_analysis()
