"""
LeetCode Scraper with Test Cases
Fetches problems with their test cases using GraphQL API
"""

import json
import requests
import time
from datetime import datetime

class LeetCodeTestCaseScraper:
    def __init__(self):
        self.base_url = "https://leetcode.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com"
        }
    
    def get_all_problems(self):
        """Get list of all problems from API"""
        print("📡 Fetching all problems from LeetCode API...")
        
        url = "https://leetcode.com/api/problems/algorithms/"
        response = requests.get(url)
        data = response.json()
        
        problems = []
        for item in data['stat_status_pairs']:
            if not item['paid_only']:  # Only free problems
                problems.append({
                    'id': item['stat']['frontend_question_id'],
                    'title': item['stat']['question__title'],
                    'slug': item['stat']['question__title_slug'],
                    'difficulty': ['Easy', 'Medium', 'Hard'][item['difficulty']['level'] - 1]
                })
        
        print(f"✓ Found {len(problems)} free problems")
        return problems
    
    def get_problem_details(self, slug):
        """Get problem details including test cases"""
        
        query = """
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            titleSlug
            content
            difficulty
            exampleTestcases
            exampleTestcaseList
            sampleTestCase
            metaData
            hints
            solution {
              id
              content
            }
            topicTags {
              name
              slug
            }
            codeSnippets {
              lang
              langSlug
              code
            }
          }
        }
        """
        
        payload = {
            "query": query,
            "variables": {"titleSlug": slug}
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            data = response.json()
            
            if 'data' in data and 'question' in data['data']:
                return data['data']['question']
            else:
                print(f"  ⚠ No data for {slug}")
                return None
                
        except Exception as e:
            print(f"  ✗ Error fetching {slug}: {e}")
            return None
    
    def parse_test_cases(self, test_case_string):
        """Parse test case string into list"""
        if not test_case_string:
            return []
        
        # Test cases are usually separated by newlines
        test_cases = []
        lines = test_case_string.strip().split('\n')
        
        for line in lines:
            if line.strip():
                test_cases.append(line.strip())
        
        return test_cases
    
    def scrape_with_test_cases(self, limit=None):
        """Main scraping function"""
        print("=" * 60)
        print("LeetCode Problem Scraper with Test Cases")
        print("=" * 60)
        
        # Get all problems
        all_problems = self.get_all_problems()
        
        if limit:
            all_problems = all_problems[:limit]
            print(f"Limiting to first {limit} problems for testing\n")
        
        results = []
        
        for i, problem in enumerate(all_problems, 1):
            print(f"\n[{i}/{len(all_problems)}] Fetching: {problem['id']}. {problem['title']}")
            
            # Get detailed problem info with test cases
            details = self.get_problem_details(problem['slug'])
            
            if details:
                # Parse test cases
                test_cases = self.parse_test_cases(details.get('exampleTestcases', ''))
                
                # Parse metadata (contains input/output format)
                metadata = {}
                try:
                    if details.get('metaData'):
                        metadata = json.loads(details['metaData'])
                except:
                    pass
                
                problem_data = {
                    'problemNumber': int(details['questionFrontendId']),
                    'title': details['title'],
                    'slug': details['titleSlug'],
                    'difficulty': details['difficulty'],
                    'content': details['content'],
                    'testCases': test_cases,
                    'sampleTestCase': details.get('sampleTestCase', ''),
                    'metaData': metadata,
                    'hints': details.get('hints', []),
                    'topicTags': [tag['name'] for tag in details.get('topicTags', [])],
                    'codeSnippets': details.get('codeSnippets', []),
                    'leetcodeUrl': f"https://leetcode.com/problems/{details['titleSlug']}/"
                }
                
                results.append(problem_data)
                print(f"  ✓ Test cases: {len(test_cases)}")
                print(f"  ✓ Topics: {', '.join(problem_data['topicTags'][:3])}")
            
            # Rate limiting - be nice to LeetCode servers
            time.sleep(2)
        
        return results
    
    def save_to_json(self, problems, filename='leetcode_with_testcases.json'):
        """Save problems to JSON file"""
        import os
        
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, filename)
        
        print(f"\n💾 Saving to {output_path}...")
        
        output = {
            'metadata': {
                'totalProblems': len(problems),
                'scrapedDate': datetime.now().isoformat(),
                'source': 'LeetCode GraphQL API',
                'difficulties': {
                    'Easy': len([p for p in problems if p['difficulty'] == 'Easy']),
                    'Medium': len([p for p in problems if p['difficulty'] == 'Medium']),
                    'Hard': len([p for p in problems if p['difficulty'] == 'Hard'])
                }
            },
            'problems': problems
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(problems)} problems with test cases!")
        print(f"\n📊 Summary:")
        print(f"   Easy: {output['metadata']['difficulties']['Easy']}")
        print(f"   Medium: {output['metadata']['difficulties']['Medium']}")
        print(f"   Hard: {output['metadata']['difficulties']['Hard']}")


def main():
    """Main execution"""
    scraper = LeetCodeTestCaseScraper()
    
    print("\nOptions:")
    print("1. Scrape ALL problems (will take 2-3 hours)")
    print("2. Scrape first 10 problems (for testing)")
    print("3. Scrape first 50 problems")
    print("4. Scrape first 100 problems")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    limit_map = {
        '1': None,
        '2': 10,
        '3': 50,
        '4': 100
    }
    
    limit = limit_map.get(choice, 10)
    
    # Scrape problems
    problems = scraper.scrape_with_test_cases(limit=limit)
    
    # Save to JSON
    scraper.save_to_json(problems)
    
    print("\n" + "=" * 60)
    print("✅ DONE!")
    print("=" * 60)
    print("\nYou now have problems with:")
    print("  • Problem descriptions")
    print("  • Test cases")
    print("  • Code templates")
    print("  • Topic tags")
    print("  • Hints")


if __name__ == "__main__":
    main()