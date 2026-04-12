"""
RAG系统评估模块
"""
import json
import os
from rag import RagService
import config_data as config


class RAGEvaluator:
    def __init__(self):
        self.rag_service = RagService()
        self.test_cases = []
    
    def load_test_cases(self, file_path):
        """加载测试用例"""
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.test_cases = json.load(f)
        else:
            # 默认测试用例
            self.test_cases = [
                {
                    "id": 1,
                    "question": "身高170厘米，体重60公斤，应该选择什么尺码？",
                    "expected_answer": "根据身高170厘米和体重60公斤，推荐选择M码。",
                    "relevance": True
                },
                {
                    "id": 2,
                    "question": "如何正确洗涤纯棉衣物？",
                    "expected_answer": "纯棉衣物应使用中性洗涤剂，水温不超过30度，轻柔手洗或机洗，避免暴晒。",
                    "relevance": True
                },
                {
                    "id": 3,
                    "question": "什么颜色的衣服适合夏天穿着？",
                    "expected_answer": "夏天适合穿着浅色衣服，如白色、浅蓝、浅粉等，这些颜色反射阳光，更凉爽。",
                    "relevance": True
                },
                {
                    "id": 4,
                    "question": "如何保养皮革制品？",
                    "expected_answer": "皮革制品应避免潮湿，定期使用皮革护理剂，存放在阴凉通风处。",
                    "relevance": True
                },
                {
                    "id": 5,
                    "question": "身高180厘米，体重90公斤，应该选择什么尺码？",
                    "expected_answer": "根据身高180厘米和体重90公斤，推荐选择XL码。",
                    "relevance": True
                }
            ]
            # 保存测试用例到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.test_cases, f, ensure_ascii=False, indent=2)
    
    def evaluate(self, test_file="test_cases.json"):
        """评估RAG系统性能"""
        self.load_test_cases(test_file)
        
        total_cases = len(self.test_cases)
        correct_answers = 0
        relevant_answers = 0
        
        results = []
        
        for test_case in self.test_cases:
            print(f"测试问题: {test_case['question']}")
            
            # 获取RAG系统回答
            response = self.rag_service.chain.invoke(
                {"input": test_case['question']}, 
                config.session_config
            )
            
            print(f"系统回答: {response}")
            print(f"期望回答: {test_case['expected_answer']}")
            
            # 简单的准确率评估（这里使用字符串包含作为简单判断）
            is_correct = test_case['expected_answer'] in response
            is_relevant = test_case['relevance']
            
            if is_correct:
                correct_answers += 1
            if is_relevant:
                relevant_answers += 1
            
            results.append({
                "question": test_case['question'],
                "system_answer": response,
                "expected_answer": test_case['expected_answer'],
                "is_correct": is_correct,
                "is_relevant": is_relevant
            })
            
            print("-" * 50)
        
        # 计算评估指标
        accuracy = correct_answers / total_cases if total_cases > 0 else 0
        relevance_rate = relevant_answers / total_cases if total_cases > 0 else 0
        
        print(f"\n评估结果:")
        print(f"测试用例总数: {total_cases}")
        print(f"正确回答数: {correct_answers}")
        print(f"准确率: {accuracy:.2f}")
        print(f"相关性比例: {relevance_rate:.2f}")
        
        # 保存评估结果
        evaluation_result = {
            "total_cases": total_cases,
            "correct_answers": correct_answers,
            "accuracy": float(accuracy),
            "relevance_rate": float(relevance_rate),
            "results": results
        }
        
        with open("evaluation_result.json", 'w', encoding='utf-8') as f:
            json.dump(evaluation_result, f, ensure_ascii=False, indent=2)
        
        print("评估结果已保存到 evaluation_result.json")
        
        return evaluation_result


if __name__ == '__main__':
    evaluator = RAGEvaluator()
    evaluator.evaluate()
