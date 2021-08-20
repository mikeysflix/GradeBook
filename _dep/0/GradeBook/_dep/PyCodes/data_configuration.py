import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from visual_configuration import *

class GradeBook(GradeBookViewer):

    def __init__(self, savedir=None, bias='left'):
        """

        """
        super().__init__(savedir, bias=bias)

    def initialize(self, readpath, name_index=None, id_index=None, email_index=None, homework_index=None, exam_index=None, extra_credit_index=None, homework_weight=None, exam_weight=None, extra_credit_weight=None, index_type='row', fail_score=None, ace_score=None, flat_curve=None, homework_curve=None, exam_curve=None, extra_credit_curve=None, max_curve=np.inf, decimals=None):
        """

        """
        ## get raw data
        raw_data = np.loadtxt(readpath, dtype=str, delimiter=',')
        ## index data by row OR column
        if index_type == 'row':
            raw_data = raw_data.T
        elif index_type != 'column':
            raise ValueError("invalid index_type: {}".format(index_type))
        ## initalize number of students
        self._number_of_students = raw_data.shape[0] - 1
        self.initialize_identifiers(raw_data, name_index, id_index, email_index)
        ## initialize weighted scores
        total_weight = self.initialize_weighted_points(raw_data, homework_index, exam_index, extra_credit_index, homework_weight, exam_weight, extra_credit_weight)
        ## initialize grading criteria
        self.initialize_grading_criteria(total_weight, fail_score, ace_score, decimals)
        ## initialize grading curve
        self.initialize_curves(flat_curve, homework_curve, exam_curve, extra_credit_curve, max_curve)
        ## initialize graded scores
        self.initialize_grade_points()
        ## get ranks of students
        ranks = self.get_ranks(self.final['score']) + 1
        ## initialize students
        self.initialize_students(ranks)

    def get_students_per_missing_score(self):
        """

        """
        result = '\nSTUDENTS PER MISSING SCORE\n\n'
        for source, item in self.points.items():
            headers = item['header']
            scores = np.isnan(item['score'])
            for i, header in enumerate(headers):
                loc = np.nonzero(scores[:, i])[0]
                if loc.size > 0:
                    result += '\n ** {} **\n'.format(header)
                    for k, j in enumerate(loc):
                        student = self.students[j]
                        for key, value in student.identifiers.items():
                            result += '\n .. ({}) {}:\t{}\n'.format(k+1, key, value)
        return result

    # def get_students_per_zero_score(self):
    #     """
    #     FIX ME !!
    #     """
    #     result = '\nSTUDENTS PER ZERO SCORE\n\n'
    #     for source, item in self.points.items():
    #         headers = item['header']
    #         scores = item['score']
    #         condition = (scores == 0)
    #         for i, header in enumerate(headers):
    #             loc = np.nonzero(condition[:, i])[0]
    #             if loc.size > 0:
    #                 result += '\n ** {} **\n'.format(header)
    #                 for k, j in enumerate(loc):
    #                     student = self.students[j]
    #                     for key, value in student.identifiers.items():
    #                         result += '\n .. ({}) {}:\t{}\n'.format(k+1, key, value)
    #     return result

    def select_student_by_prompt(self, identifiers=None):
        """

        """
        ## select single identifier by priority and convenience of use
        if identifiers is None:
            for key in ('id number', 'name', 'email'):
                if key in list(self.identifiers.keys()):
                    identifiers = [key]
                    break
            if identifiers is None:
                raise ValueError("identifiers are not intialized")
        ## select single identifier
        elif isinstance(identifiers, str):
            identifiers = [identifiers]
        ## select multiple identifiers
        elif isinstance(identifiers, (tuple, list, np.ndarray)):
            for identifier in identifiers:
                if identifier not in ('id number', 'name', 'email'):
                    raise ValueError("identifiers contains an invalid element: {}".format(identifier))
        else:
            raise ValueError("invalid type(identifiers): {}".format(type(identifiers)))
        ## initialize locations
        locs = set()
        for identifier in identifiers:
            ## get user input
            test_value = str(input("please enter your {}:       ".format(identifier)))
            ## get index number of student
            i = self.get_student_index(identifier, test_value)
            ## add index number to unique set
            locs.add(i)
        if len(locs) != 1:
            raise ValueError("student index number should be the same for all identifiers")
        return self.students[next(iter(locs))]

    def get_all_attachments(self):
        """

        """
        attachments = []
        if self.savedir is not None:
            for filename in os.listdir(self.savedir):
                filepath = '{}{}'.format(self.savedir, filename)
                attachments.append(filepath)
        if len(attachments) == 0:
            return None
        else:
            return attachments

    def email_students(self, students=None, show_assignments=False, show_grade=False, show_rank=False, attachments=None, port=587):
        """
        https://nitratine.net/blog/post/how-to-send-an-email-with-python/#attachments

        https://stackoverflow.com/questions/13070038/attachment-image-to-send-by-mail-using-python

        https://www.knowledgehut.com/tutorials/python-tutorial/python-send-email

        https://www.javacodemonk.com/python-send-gmail-with-attachment-fba8bbe4
        """
        ## log into account
        username = str(input("please enter your email address:      "))
        password = str(input("please enter your password:      "))
        server = smtplib.SMTP('smtp.gmail.com', port)
        # server.ehlo()
        server.starttls()
        # server.ehlo()
        server.login(username, password)
        ## more than one student, recursive
        if students is None: ## all students, recursive
            for student in self.students:
                self.email_students(student, show_assignments, show_grade, show_rank, attachments)
        elif isinstance(students, (tuple, list, np.ndarray)): ## multiple students, recursive
            for student in students:
                self.email_students(student, show_assignments, show_grade, show_rank, attachments)
        ## main function, single student
        else:
            if not isinstance(students, Student): ## via instance
                if isinstance(students, int): ## via index number
                    students = self.students[students]
                else:
                    raise ValueError("invalid type(students): {}".format(type(students)))
            ## initialize email message
            msg = MIMEMultipart()
            msg['From'] = username ## sender
            msg['To'] = students.identifiers['email'] ## recipient
            msg['Subject'] = "Progress Report" ## subject-line
            ## add body text to email message
            if 'name' in list(students.identifiers.keys()):
                intro = 'Hello {}, I hope you are having a wonderful day. \
                        The text below shows how many points you have earned.'.format(students.identifiers['name'])
            else:
                intro = 'Hello. The text below shows how many points you have earned.'
            show_identifiers = True
            s = students.get_string(show_identifiers, show_assignments, show_grade, show_rank)
            body = '{}\n{}'.format(intro, s)
            msg.attach(MIMEText(body, 'plain'))
            ## add attachments to email message
            if attachments is not None:
                if isinstance(attachments, str):
                    attachments = [attachments]
                if isinstance(attachments, (tuple, list, np.ndarray)):
                    for filepath in attachments:
                        with open(filepath, 'rb') as img:
                            msg.attach(MIMEImage(img.read(), name=os.path.basename(filepath)))
                else:
                    raise ValueError("invalid type(attachments): {}".format(type(attachments)))
            ## send email
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        ## log out of connection
        server.quit()

##
