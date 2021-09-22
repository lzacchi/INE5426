-- Program that calculates the average notes
-- from an array of students

{
  int n_students;
  n_students = 10;

  int n_tests;
  n_tests = 4;

  string student_name;
  student_name = new string[n_students];

  float student_test_grade;
  student_test_grade = new float[n_students][n_tests];

  int birth_year;
  birth_year = new int[n_students];

  int base_year;
  base_year = 1990;

  print "defining functions";
  print "initializing students";

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


  int i;
  for (i = 0; i < n_students; i=i+1){
    print "set birth year:";
    birth_year[i] = (base_year);
  }

  print "set random tests scores";
  int j;
  for (i=0; i < n_students; i=i+1){
    for (j=0; j < n_tests; j=j+1){
      student_test_grade[i][j] = (n_tests * 6);
    }

  }

  print "Calculating grades";

  float grades;
  grades = new float[n_students];

  for (i=0; i < n_students; i=i+1){
    float sum;
    sum = 0;
    for (j=0; j < n_tests; j=j+1){
      sum = sum + student_test_grade[i][j];
    }

    print "saving grade";
    grades[i] = sum/n_tests;
  }

  print "Done!";

  print "Printing all students grades:";

  for (i=0; i < n_students; i=i+1){
    print "------------------------";
    print "STUDENT: " ;
    print  student_name[i];
    for (j=0; j < n_tests; j=j+1){
      print "Test ";
      print j;
      print " score: ";
      print student_test_grade[i][j];
    }

    print "Grade: ";
    print grades[i];

    if (grades[i] >= 6){
      print "Congratulations, ";
      print student_name[i];
      print ". You are approved!";
    } else {
      print "Sorry, ";
      print student_name[i];
      print " :( you are not approved.";
      print "Try again next year :D";
    }

    print "----------------------";
  }
  print "Ending program...";
  return;
}
