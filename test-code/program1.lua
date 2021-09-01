--
-- program1.lua
--
-- Authors: Artur Barichello
--          Lucas Verdade
--          Lucas Zacchi
--

-- Exemplo 1
-- Algoritmo: Declarar e inicializar os alunos de uma turma.
--            Gerar as notas dos testes pra cada um e calcular a média.
--            Apresentar o nome, notas, média e se passou na matéria ao final.

-- Declaring and initialazing variables
{
  int n_students;
  n_students = 10;

  int n_tests;
  n_tests = 4;

  string student_name;
  student_name = new string[n_students];

  float student_test_grade;
  student_test_grade = new float[n_students][n_tests];

  int i;

  int birth_year;
  birth_year = new int[n_students];

  int base_year;
  base_year = 1990;

-- defining functions
  -- initialazing students

  student_name[0] = "Artur";
  student_name[1] = "Lucas V";
  student_name[2] = "Lucas Z";
  student_name[3] = "Afonso";
  student_name[4] = "Alonso";
  student_name[5] = "Antonio";
  student_name[6] = "Alberta";
  student_name[7] = "Juliana";
  student_name[8] = "Patricia";
  student_name[9] = "Francisco";


  for (i = 0; i < n_students; i++){
    -- set birth year
    birth_year[i] = (base_year + i);
  }

  -- set random tests scores
  int j;
  for (i=0; i < n_students; i++){
    for (j=0; j < n_tests; j++){
      student_test_grade[i][j] = (n_tests * 5.75 + i) % 10; -- set random score
    }

  }

  print("Calculating grades");

  float grades;
  grades = new float[n_students];

  for (i=0; i < n_students; i++){
    float sum;
    sum = 0;
    for (j=0; j < n_tests; j++){
      sum = sum + student_test_grade[i][j];
    }

    -- saving grade
    grades[i] = sum/n_tests;
  }

  print("Done!");

  print("Printing all students grades:");

  for (i=0; i < n_students; i++){
    print("--------------------");
    print("STUDENT: " + student_name[i]);
    for (j=0; j < n_tests; j++){
      print("Test " + j + " score: " + student_test_grade[i][j]);
    }

    print("Grade: "+ grades[i]);

    if (grades[i] >= 5.75){
      print("Congratulations, "+ student_name[i]  +". You are approved!");
    } else {
      print("Sorry, " + student_name[i] + " :( you are not approved. Try again next year :D");
    }

    print("--------------------");
  }
  print("Ending program...")
  return;
-- run:
}