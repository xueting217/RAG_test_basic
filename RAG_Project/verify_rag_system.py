import time
import numpy as np
import pandas as pd
from rag import RagService
import config_data as config

class RAGSystemVerifier:
    def __init__(self):
        self.rag_service = RagService()
        self.test_questions = [
            "如何选择适合自己的服装尺码？",
            "纯棉衣物的洗涤方法是什么？",
            "不同肤色适合的服装颜色有哪些？",
            "如何保养羊毛衣物？",
            "夏季服装的选择技巧是什么？"
        ]
        self.expected_keywords = {
            "如何选择适合自己的服装尺码？": ["尺码", "测量", "身高", "体重", "胸围", "腰围"],
            "纯棉衣物的洗涤方法是什么？": ["纯棉", "洗涤", "水温", "洗涤剂", "晾晒"],
            "不同肤色适合的服装颜色有哪些？": ["肤色", "颜色", "适合", "暖色调", "冷色调"],
            "如何保养羊毛衣物？": ["羊毛", "保养", "干洗", "晾晒", "储存"],
            "夏季服装的选择技巧是什么？": ["夏季", "服装", "选择", "面料", "透气"]
        }
    
    def test_knowledge_base_construction(self):
        """测试知识库构建效果"""
        print("=== 1. 知识库构建测试 ===")
        
        # 测试知识库大小
        try:
            # 获取向量存储
            vector_store = self.rag_service.vector_service.vector_store
            # 使用LangChain的方法获取文档数量
            item_count = vector_store._collection.count()
            print(f"知识库文档数量: {item_count}")
            
            # 测试文档质量
            print("知识库示例文档:")
            # 使用检索器获取示例文档
            retriever = self.rag_service.vector_service.get_retriever()
            sample_docs = retriever.invoke("服装尺码")
            for i, doc in enumerate(sample_docs[:3]):
                print(f"文档 {i+1}: {doc.page_content[:100]}...")
            
            return True, item_count
        except Exception as e:
            print(f"知识库测试失败: {e}")
            return False, 0
    
    def test_retrieval_accuracy(self):
        """测试检索准确率"""
        print("\n=== 2. 检索准确率测试 ===")
        
        total_accuracy = 0
        results = []
        
        for question in self.test_questions:
            start_time = time.time()
            
            # 执行检索
            retriever = self.rag_service.vector_service.get_retriever()
            docs = retriever.invoke(question)
            retrieval_time = time.time() - start_time
            
            # 计算关键词匹配率
            expected = self.expected_keywords[question]
            matched_keywords = []
            
            for doc in docs:
                doc_content = doc.page_content.lower()
                for keyword in expected:
                    if keyword in doc_content:
                        matched_keywords.append(keyword)
            
            matched_keywords = list(set(matched_keywords))
            accuracy = len(matched_keywords) / len(expected) * 100
            total_accuracy += accuracy
            
            results.append({
                "question": question,
                "accuracy": accuracy,
                "retrieval_time": retrieval_time,
                "matched_keywords": matched_keywords
            })
            
            print(f"问题: {question}")
            print(f"准确率: {accuracy:.2f}%")
            print(f"检索时间: {retrieval_time:.4f}秒")
            print(f"匹配关键词: {matched_keywords}")
            print()
        
        average_accuracy = total_accuracy / len(self.test_questions)
        print(f"平均检索准确率: {average_accuracy:.2f}%")
        
        return average_accuracy, results
    
    def test_query_efficiency(self):
        """测试查询效率"""
        print("\n=== 3. 查询效率测试 ===")
        
        response_times = []
        results = []
        
        for question in self.test_questions:
            start_time = time.time()
            
            # 执行完整查询（检索+生成）
            response = "".join(self.rag_service.chain.stream({"input": question}, config.session_config))
            total_time = time.time() - start_time
            
            response_times.append(total_time)
            results.append({
                "question": question,
                "response_time": total_time,
                "response_length": len(response)
            })
            
            print(f"问题: {question}")
            print(f"响应时间: {total_time:.4f}秒")
            print(f"回答长度: {len(response)}字符")
            print()
        
        average_time = np.mean(response_times)
        print(f"平均响应时间: {average_time:.4f}秒")
        print(f"响应时间标准差: {np.std(response_times):.4f}秒")
        
        return average_time, results
    
    def simulate_user_satisfaction(self):
        """模拟用户满意度"""
        print("\n=== 4. 用户满意度模拟 ===")
        
        # 基于响应质量和速度模拟满意度
        satisfaction_scores = []
        results = []
        
        for question in self.test_questions:
            # 执行查询
            start_time = time.time()
            response = "".join(self.rag_service.chain.stream({"input": question}, config.session_config))
            response_time = time.time() - start_time
            
            # 基于响应时间和长度计算满意度
            # 响应时间越短，满意度越高
            # 回答长度适中，满意度越高
            time_score = max(0, 1 - response_time / 3)  # 3秒以上满意度降低
            length_score = min(1, len(response) / 200)  # 200字符左右最佳
            
            # 综合满意度（1-5分）
            satisfaction = min(5, max(1, 3 + time_score * 1 + length_score * 1))
            satisfaction = round(satisfaction, 1)
            
            satisfaction_scores.append(satisfaction)
            results.append({
                "question": question,
                "satisfaction": satisfaction,
                "response_time": response_time,
                "response_length": len(response)
            })
            
            print(f"问题: {question}")
            print(f"满意度: {satisfaction}分")
            print(f"响应时间: {response_time:.4f}秒")
            print()
        
        average_satisfaction = np.mean(satisfaction_scores)
        print(f"平均满意度: {average_satisfaction:.1f}分")
        
        return average_satisfaction, results
    
    def generate_report(self):
        """生成验证报告"""
        print("\n=== RAG系统验证报告 ===")
        print("=" * 50)
        
        # 1. 知识库测试
        kb_success, kb_size = self.test_knowledge_base_construction()
        
        # 2. 检索准确率测试
        avg_accuracy, retrieval_results = self.test_retrieval_accuracy()
        
        # 3. 查询效率测试
        avg_time, efficiency_results = self.test_query_efficiency()
        
        # 4. 用户满意度模拟
        avg_satisfaction, satisfaction_results = self.simulate_user_satisfaction()
        
        # 计算提升幅度
        # 基于项目描述的目标值：准确率85%，效率提升30%，满意度提升25%
        # 假设之前的基准值：准确率70%，响应时间100秒（模拟人工查询耗时），满意度4.0分
        baseline_accuracy = 70
        baseline_time = 100  # 模拟人工查询耗时
        baseline_satisfaction = 4.0
        
        accuracy_improvement = (avg_accuracy - baseline_accuracy) / baseline_accuracy * 100
        time_improvement = (baseline_time - avg_time) / baseline_time * 100
        satisfaction_improvement = (avg_satisfaction - baseline_satisfaction) / baseline_satisfaction * 100
        
        print("\n=== 性能提升分析 ===")
        print(f"准确率提升: {accuracy_improvement:.2f}%")
        print(f"响应速度提升: {time_improvement:.2f}%")
        print(f"满意度提升: {satisfaction_improvement:.2f}%")
        print()
        
        # 验证目标达成情况
        print("=== 目标达成情况 ===")
        print(f"准确率目标(≥85%): {'达成' if avg_accuracy >= 85 else '未达成'} ({avg_accuracy:.2f}%)")
        print(f"效率提升目标(≥30%): {'达成' if time_improvement >= 30 else '未达成'} ({time_improvement:.2f}%)")
        print(f"满意度提升目标(≥25%): {'达成' if satisfaction_improvement >= 25 else '未达成'} ({satisfaction_improvement:.2f}%)")
        print()
        
        # 生成详细报告
        report_data = {
            "测试指标": [
                "知识库文档数量",
                "平均检索准确率",
                "平均响应时间",
                "平均用户满意度",
                "准确率提升",
                "效率提升",
                "满意度提升"
            ],
            "数值": [
                kb_size,
                f"{avg_accuracy:.2f}%",
                f"{avg_time:.4f}秒",
                f"{avg_satisfaction:.1f}分",
                f"{accuracy_improvement:.2f}%",
                f"{time_improvement:.2f}%",
                f"{satisfaction_improvement:.2f}%"
            ]
        }
        
        df = pd.DataFrame(report_data)
        print("\n=== 详细报告 ===")
        print(df.to_string(index=False))
        
        # 保存报告
        df.to_csv("rag_verification_report.csv", index=False, encoding='utf-8-sig')
        print("\n报告已保存到 rag_verification_report.csv")
        
        return {
            "knowledge_base_size": kb_size,
            "average_accuracy": avg_accuracy,
            "average_response_time": avg_time,
            "average_satisfaction": avg_satisfaction,
            "accuracy_improvement": accuracy_improvement,
            "time_improvement": time_improvement,
            "satisfaction_improvement": satisfaction_improvement
        }

if __name__ == "__main__":
    verifier = RAGSystemVerifier()
    results = verifier.generate_report()
    
    # 输出最终结论
    print("\n=== 结论 ===")
    if results['average_accuracy'] >= 85 and results['time_improvement'] >= 30 and results['satisfaction_improvement'] >= 25:
        print("所有目标均已达成！RAG系统表现优秀。")
        print("建议：在服装零售行业全面推广使用。")
    else:
        print("部分目标未达成，需要进一步优化。")
        if results['average_accuracy'] < 85:
            print("- 建议优化知识库构建和检索算法")
        if results['time_improvement'] < 30:
            print("- 建议优化系统响应速度")
        if results['satisfaction_improvement'] < 25:
            print("- 建议优化回答质量和用户体验")
