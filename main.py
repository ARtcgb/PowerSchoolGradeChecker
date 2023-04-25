from GradeChecker import GradeChecker

if __name__ == '__main__':
    json_file_path = "data.json"
    properties_path = 'config/config.properties'
    grade_checker = GradeChecker(properties_path, json_file_path)
    grade_checker.run()
