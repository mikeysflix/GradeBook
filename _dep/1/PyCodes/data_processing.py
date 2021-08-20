from collections import OrderedDict
import numpy as np
import scipy.stats as SPstats
import os
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class DistanceMatrix():

    def __init__(self):
        """

        """
        super().__init__()
        self.distance_metrics = {
            'manhattan' : self.get_manhattan_distance,
            'euclidean' : self.get_euclidean_distance,
            'euclidean square' : self.get_euclidean_square_distance}
        self._f = None

    @property
    def f(self):
        return self._f

    @staticmethod
    def get_manhattan_distance(displacement, axis=None):
        """

        """
        return np.nansum(np.abs(displacement), axis=axis)

    @staticmethod
    def get_euclidean_square_distance(displacement, axis=None):
        """

        """
        return np.nansum(np.square(displacement), axis=axis)

    def get_euclidean_distance(self, displacement, axis=None):
        """

        """
        return np.sqrt(self.get_euclidean_square_distance(displacement, axis))

    def update_distance_metric(self, distance_metric):
        """

        """
        if distance_metric not in list(self.distance_metrics.keys()):
            raise ValueError("invalid distance_metric: {}".format(distance_metric))
        self._f = self.distance_metrics[distance_metric]

    def get_distance_matrix(self, arr, mask_diagonal=False):
        """

        """
        if isinstance(arr, (tuple, list)):
            arr = np.array(arr)
        if not isinstance(arr, np.ndarray):
            raise ValueError("invalid type(arr): {}".format(type(arr)))
        if arr.ndim == 1:
            coordinates = np.array([arr, np.zeros(arr.size)]).T
        else:
            coordinates = np.array(arr)
        shape = (coordinates.shape[0], 1, coordinates.shape[1])
        displacement = coordinates - coordinates.reshape(shape)
        result = self.f(
            displacement=displacement,
            axis=-1)
        if mask_diagonal:
            loc = np.eye(*result.shape)
            result = np.ma.masked_where(loc, result)
        return result

class Student():

    def __init__(self, identifiers, points, rank):
        """

        """
        super().__init__()
        self.identifiers = identifiers
        self.points = points
        self.rank = rank

    def __repr__(self):
        return "Student(%r, %r, %r)" % (self.identifiers, self.points, self.rank)

    def __str__(self):
        s = self.get_string(
            show_identifiers=True,
            show_assignments=True,
            show_grade=True,
            show_rank=True)
        return s

    def get_string(self, show_identifiers=False, show_assignments=False, show_grade=False, show_rank=False):
        """

        """
        s = ""
        if show_identifiers:
            s += "- "*10 + "\n\tidentifiers\n" + "- "*10
            for key, value in self.identifiers.items():
                s += "\n .. {}:\n{}\n".format(key, value)
        if show_assignments:
            for key, value in self.points.items():
                if key in ('homework', 'exam', 'extra credit'):
                    s += "- "*10 + "\n\t{}\n".format(key) + "- "*10
                    for inner_key, inner_value in value.items():
                        s += "\n .. {}:\n{} / {}\n".format(inner_key, inner_value['score'], inner_value['weight'])
                elif key == 'curve':
                    s += "- "*10 + "\n\tcurve\n" + "- "*10
                    for inner_key, inner_value in value.items():
                        s += "\n .. {}:\n{}\n".format(inner_key, inner_value)
        if show_grade:
            s += "- "*10 + "\n\tfinal\n" + "- "*10
            item = self.points['final']
            s += "\n .. Grade:\n{}, {}\n".format(item['score'], item['grade'])
        if show_rank:
            s += "- "*10 + "\n\trank\n" + "- "*10
            s += "\n .. rank:\n{}\n".format(self.rank['message'])
        return s

class DataInitialization():

    def __init__(self):
        """

        """
        super().__init__()
        self._raw_data = None
        self._number_of_students = None
        self._identifiers = dict()
        self._points = OrderedDict()
        self._total_weight = None

    @property
    def raw_data(self):
        return self._raw_data

    @property
    def number_of_students(self):
        return self._number_of_students

    @property
    def identifiers(self):
        return self._identifiers

    @property
    def points(self):
        return self._points

    @property
    def total_weight(self):
        return self._total_weight

    def initialize_raw_data(self, fpath):
        """

        """
        extension = Path(fpath).suffix
        if extension == '.csv':
            raw_data = np.loadtxt(fpath, dtype=str, delimiter=',')
        else:
            raise ValueError("not yet implemented")
        self._raw_data = raw_data

    def finalize_raw_data(self, index_by):
        """

        """
        if index_by == 'row':
            self._raw_data = self._raw_data.T
        elif index_by != 'column':
            raise ValueError("invalid index_by: {}".format(index_by))
        self._number_of_students = self.raw_data.shape[0] - 1

    def initialize_identifiers(self, name_loc=None, id_loc=None, email_loc=None):
        """

        """
        identifiers = dict()
        for key, i in zip(('name', 'id number', 'email'), (name_loc, id_loc, email_loc)):
            if isinstance(i, int):
                identifiers[key] = np.copy(self.raw_data[1:, i])
            elif i is not None:
                raise ValueError("invalid type(index): {}".format(type(i)))
        if len(identifiers) == 0:
            raise ValueError("input at least one identifier: 'name_loc', 'id_loc', 'email_loc'")
        self._identifiers.update(identifiers)

    @staticmethod
    def get_statistics(arr, axis=None, ddof=0):
        """

        """
        ## ungraded assignments are NaN
        fmap = {
            'minimum' : np.nanmin(arr, axis=axis),
            'maximum' : np.nanmax(arr, axis=axis),
            'mean' : np.nanmean(arr, axis=axis),
            'median' : np.nanmedian(arr, axis=axis),
            'standard deviation' : np.nanstd(arr, axis=axis, ddof=ddof),
            'mode' : SPstats.mode(arr, axis=axis, nan_policy='omit'),
            'total' : np.nansum(arr, axis=axis),
            # 'n missing' : np.isnan(arr, axis=axis),
            # 'n zero' : len(arr[..., ...]) - arr.count_nonzero(axis=axis),
                }
        return OrderedDict(sorted(fmap.items()))

    def initialize_weighted_points(self, homework_loc=None, exam_loc=None, extra_credit_loc=None, homework_weight=None, exam_weight=None, extra_credit_weight=None):
        """

        """
        if all(i is None for i in (homework_loc, exam_loc, extra_credit_loc)):
            raise ValueError("input at least one loc: 'homework_loc', 'exam_loc', 'extra_credit_loc'")
        total_weight = 0
        for key, i, weight in zip(('homework', 'exam', 'extra credit'), (homework_loc, exam_loc, extra_credit_loc), (homework_weight, exam_weight, extra_credit_weight)):
            if i is not None:
                if weight is None:
                    raise ValueError("assignment weight cannot be None")
                ## weights for single assignment
                if isinstance(i, int):
                    if isinstance(weight, (int, float)):
                        wres = np.array([wt])
                    else:
                        raise ValueError("invalid type(weight)={} for single assignment".format(weight))
                ## weights for multiple assignments
                elif isinstance(i, (tuple, list, np.ndarray)):
                    if isinstance(weight, (int, float)):
                        wres = np.array([weight]*len(i))
                    else:
                        n, m = len(weight), len(i)
                        if n != m:
                            raise ValueError("{} weights are not compatible with {} assignments".format(n, m))
                        wres = np.array(weight)
                else:
                    raise ValueError("invalid type for index element: {}".format(type(i)))
                header = np.copy(self.raw_data[0, i])
                scores = np.copy(self.raw_data[1:, i]).astype(float)
                statistics = self.get_statistics(scores, axis=0)
                total_weight += np.nansum(wres)
                self._points[key] = {
                    'header' : header,
                    'score' : scores,
                    'weight' : wres,
                    'statistics' : statistics,
                    'total' : np.nansum(scores, axis=1)}
        self._total_weight = total_weight

class GradePointAnalysis(DataInitialization):

    def __init__(self, bias='left'):
        """

        """
        super().__init__()
        if bias not in ('left', 'right'):
            raise ValueError("invalid bias: {}".format(bias))
        self.bias = bias
        self.letters = np.array(['F', 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+'])
        self._final = OrderedDict()
        self._grading_criteria = dict()
        self._grade_ranks = None
        self._students = list()

    @property
    def final(self):
        return self._final

    @property
    def grading_criteria(self):
        return self._grading_criteria

    @property
    def grade_ranks(self):
        return self._grade_ranks

    @property
    def students(self):
        return self._students

    @staticmethod
    def get_ranks(arr):
        """

        """
        sidx = np.argsort(arr, kind='mergesort')
        idx = np.concatenate(([0], np.flatnonzero(np.diff(arr[sidx]))+1, [arr.size]))
        inv_ranks = np.repeat(idx[:-1], np.diff(idx))[sidx.argsort()]
        return np.argsort(inv_ranks)[::-1]

    def initialize_grading_criteria(self, fail_score=None, ace_score=None, decimals=None):
        """

        """
        ## get fail/ace scores
        if ace_score is None:
            ace_score = 0.95 * self.total_weight
        if fail_score is None:
            fail_score = ace_score / 2
        if fail_score >= ace_score:
            raise ValueError("fail_score ({}) must be less than ace_score ({})".format(fail_score, ace_score))
        ## get bin-edges for grades between ace and fail
        middle_edges = np.linspace(fail_score, ace_score, self.letters.size-1)
        edges = np.array([-1] + middle_edges.tolist() + [self.total_weight * 10])
        if decimals is not None:
            edges = np.round(edges, decimals=decimals)
        ## get message
        f = lambda lb, ub, grade : '{} ≤ score < {}:\n\t{}\n'.format(lb, ub, grade) if self.bias == 'left' else '{} < score ≤ {}:\n\t{}'.format(lb, ub, grade)
        sub_strings = []
        for idx, (lbound, ubound, grade) in enumerate(zip(edges[:-1], edges[1:], self.letters)):
            if idx == self.letters.size - 1:
                lb, ub = lbound, 'infinity'
            else:
                lb, ub = lbound, ubound
            s = f(lb, ub, grade)
            sub_strings.append(s)
        msg = '\n** GRADE BOUNDARIES (bias={})\n'.format(self.bias) + '='*10 + '\n' + '\n'.join(sub_strings)
        ## initialize grading criteria
        self._grading_criteria.update({
            # 'weight' : self.total_weight,
            'fail' : fail_score,
            'ace' : ace_score,
            'edges' : edges,
            'message' : msg})

    def initialize_curves(self, flat_curve=None, homework_curve=None, exam_curve=None, extra_credit_curve=None, max_curve=np.inf):
        """

        """
        tally = np.zeros(self.number_of_students)
        scores, headers = [], []
        is_curved = False
        ## apply flat curve for all students
        if flat_curve is not None:
            is_curved = True
            if isinstance(flat_curve, (int, float)):
                flat_curve = np.ones(self.number_of_students) * flat_curve
            else:
                raise ValueError("invalid type(flat_curve): {}".format(type(flat_curve)))
            headers.append('flat')
            scores.append(flat_curve)
            tally += flat_curve
        ## apply curves based on improvement
        for key, scale in zip(('homework', 'exam', 'extra credit'), (homework_curve, exam_curve, extra_credit_curve)):
            if scale is not None:
                is_curved = True
                weight = self.points[key]['weight']
                if weight.size > 1:
                    unweighted_scores = self.points[key]['score']
                    weighted_scores = unweighted_scores / weight
                    i = weight.size // 2 # separate halves
                    first_half = np.nanmean(weighted_scores[:, :i], axis=1)
                    second_half = np.nanmean(weighted_scores[:, i:], axis=1)
                    delta = second_half - first_half
                    delta[delta < 0] = 0
                    bonus_curve = delta * np.nanmean(weight) * scale
                    tally += bonus_curve
                    # headers.append('{} curve'.format(key))
                    headers.append(key)
                    scores.append(bonus_curve)
                else:
                    raise ValueError("cannot curve {} based on improvement since only one {} exists".format(key, key))
        ## initialize curves
        if is_curved:
            ## verify total curve
            tally[tally > max_curve] = max_curve
            scores = np.array(scores)
            self._points['curve'] = {
                'header' : np.array(headers),
                'score' : scores.T,
                'statistics' : self.get_statistics(scores, axis=1),
                'total' : tally}

    def get_grades(self, scores):
        """

        """
        indices = np.searchsorted(self.grading_criteria['edges'], scores, side=self.bias) - 1
        return np.copy(self.letters)[indices]

    def initialize_grade_points(self):
        """

        """
        ## homework + exam + extra credit + curve
        point_scores = np.nansum([value['total'] for key, value in self.points.items()], axis=0)
        ## grade
        self._final['score'] = point_scores
        self._final['grade'] = self.get_grades(point_scores)
        self._final['statistics'] = self.get_statistics(point_scores, axis=None)

    def initialize_grade_ranks(self):
        """

        """
        self._grade_ranks = self.get_ranks(self.final['score']) + 1

    def initialize_students(self):
        """

        """
        ## iterate through data
        for i in range(self.number_of_students):
            ## initialize identifiers
            identifiers = {key : value[i] for key, value in self.identifiers.items()}
            ## iniitialize points
            pts = OrderedDict()
            ## homework + exam + extra credit + curve
            for key, value in self.points.items():
                assignment = OrderedDict()
                if key == 'curve':
                    for j, header in enumerate(self.points['curve']['header']):
                        assignment[header] = self.points['curve']['score'][i, j]
                else:
                    for j, header in enumerate(self.points[key]['header']):
                        assignment[header] = {
                            'weight' : self.points[key]['weight'][j],
                            'score' : self.points[key]['score'][i, j]}
                pts[key] = assignment
            ## grade-points
            final = OrderedDict()
            for key in ('score', 'grade'):
                final[key] = self.final[key][i]
            pts['final'] = final
            ## class-wide ranking
            rank = {
                'numeric' : self.grade_ranks[i],
                'message' : '{}/{}'.format(self.grade_ranks[i], self.number_of_students)}
            ## initialize student
            student = Student(identifiers, pts, rank)
            self._students.append(student)
        self._students = np.array(self._students)

class StudentInteractionMethods(GradePointAnalysis):

    def __init__(self, bias='left'):
        """

        """
        super().__init__(bias=bias)

    @staticmethod
    def get_all_attachments(savedir=None):
        """

        """
        attachments = []
        if savedir is not None:
            for filename in os.listdir(savedir):
                filepath = '{}{}'.format(savedir, filename)
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

    def get_student_index(self, identifier, test_value):
        """

        """
        condition = (self.identifiers[identifier] == test_value)
        if np.any(condition):
            loc = np.nonzero(condition)[0]
            if loc.size > 1:
                raise ValueError("multiple students share the same {} '{}'".format(identifier, test_value))
        else:
            raise ValueError("{} is not a valid {}; student not found".format(test_value, identifier))
        return loc[0]

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

##






##
