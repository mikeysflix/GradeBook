# GradeBook

Minimum Requirements:

    Python 3.9.4

    --> numpy==1.20.2

    --> matplotlib==3.4.1

    --> scipy==1.6.2

    --> pandas==1.2.4 (optional)

    --> networkx==2.5.1 (optional)

**Synopsis:**

Maintaining a gradebook can take a lot of time; this code is meant to simplify the process for an instructor. This code contains methods to track missed assingments, tally student points, apply curves, and assign grades. This code is meant to serve as a back-end; I would like to add UI front-end in a future update. A fake dataset (containing names of characters from stand-up comedy, TV shows, and video games) was used to generate the output below; this can be reproduced by substituting the relevant file-paths in and running `application.py`.

Depending on your preference, the data should be formatted as '.csv', '.txt', or '.xlsx'. In the sample data provided, there are headers that index each column - this is the default, but one has the option of indexing by row instead; in either case, one shoudl count indices starting from zero. This sample data represents points earned per student; there are ten homework assignments (each worth ten points), and two exams (one 30-point quiz and one 45-point test). Below is a table of this sample data.

<>
put picture of data table here
<>

When evaluating student points, one has the option of applying curves. The first type of curve is a flat curve that is applied equally to all students. Another type of curve is specified by assignment type ('homework', 'exam', or 'extra credit'); this method checks for improvement by comparing the latter half of assignment points against the initial half of assignment points and assigns points accordingly. The figures below were generated from the sample data, and are meant to serve as an example of the output; some figures are not shown below for sake of brevity (such as network diagrams, pie-charts, heat-maps, and duplicates of plot-styles shown below for different assignments), but can be found in the '/Figures' in the root directory in this repository.

![Histogram of Homework 1 Scores](https://github.com/mikeysflix/GradeBook/blob/master/Figures/histogram_distribution_homework_HW_1.png?raw=true)

![Box-Plot of All Homework Scores](https://github.com/mikeysflix/GradeBook/blob/master/boxplot_homework.png?raw=true)

![Histogram of Assigned Grades](https://github.com/mikeysflix/GradeBook/blob/main/histogram_distribution_grade.png?raw=true)

![Stacked Bar-Chart of Scores per Student](https://github.com/mikeysflix/GradeBook/blob/main/stacked_homework_exam_curve.png?raw=true)

Note that in the stacked bar-chart shown just above, there is only student with over 100% of the maximum allowed points - this is because this student has perfect scores on every assignment (which means no points were earned from the improvement curve) and earned additional points from the flat curve.

**Things To Add:**

The base functionality for email is set-up, but has not yet been fully tested and debugged. This can be useful to send periodic updates to the class regarding individual points per assignment, class-wide statistics per assignment, and notifications regarding missed assignments.




#
