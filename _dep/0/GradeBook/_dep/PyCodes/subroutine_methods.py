from collections import OrderedDict
import numpy as np
from scipy.stats import mode

class Student():

    def __init__(self, identifiers, points, rank):
        """

        """
        super().__init__()
        self.identifiers = identifiers
        self.points = points
        self.rank = rank

    def __str__(self):
        result = ''
        for key, value in self.identifiers.items():
            result += '{}:\n{}\n'.format(key, value)
        return result

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

    def reveal(self, show_identifiers=False, show_assignments=False, show_grade=False, show_rank=False):
        """

        """
        s = self.get_string(show_identifiers, show_assignments, show_grade, show_rank)
        print(s)

class DistanceMatrix():

    def __init__(self):
        """

        """
        super().__init__()
        self.fmap = {
            'manhattan' : self.get_manhattan_distance,
            'euclidean' : self.get_euclidean_distance,
            'euclidean square' : self.get_euclidean_square_distance
                        }

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

    def get_distance_matrix(self, arr, distance_metric, mask_diagonal=False):
        """

        """
        if distance_metric not in list(self.fmap.keys()):
            raise ValueError("invalid distance_metric: {}".format(distance_metric))
        f = self.fmap[distance_metric]
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
        result = f(displacement, axis=-1)
        if mask_diagonal:
            loc = np.eye(*result.shape)
            result = np.ma.masked_where(loc, result)
        return result

class SubRoutines(DistanceMatrix):

    def __init__(self, bias='left'):
        """

        """
        super().__init__()
        if bias not in ('left', 'right'):
            raise ValueError("invalid bias: {}".format(bias))
        self.bias = bias
        self.letters = np.array(['F', 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+'])
        self._identifiers = dict()
        self._points = OrderedDict()
        self._final = OrderedDict()
        self._grading_criteria = dict()
        self._students = list()
        self._number_of_students = None

    @property
    def identifiers(self):
        return self._identifiers

    @property
    def points(self):
        return self._points

    @property
    def final(self):
        return self._final

    @property
    def grading_criteria(self):
        return self._grading_criteria

    @property
    def students(self):
        return self._students

    @property
    def number_of_students(self):
        return self._number_of_students

    @staticmethod
    def select_percents(percents):
        """

        """
        if isinstance(percents, (int, float)):
            percents = np.array([percents])
        elif isinstance(percents, (tuple, list)):
            percents = np.array(percents)
        elif not isinstance(percents, np.ndarray):
            raise ValueError("invalid type(percents): {}".format(type(percents)))
        if np.any(percents < 0):
            raise ValueError("percents must be non-negative")
        if np.any(percents > 100):
            raise ValueError("percents cannot exceed 100")
        return percents

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
            'mode' : mode(arr, axis=axis, nan_policy='omit'),
            'total' : np.nansum(arr, axis=axis),
            # 'n missing' : np.isnan(arr, axis=axis),
            # 'n zero' : len(arr[..., ...]) - arr.count_nonzero(axis=axis),
                }
        return OrderedDict(sorted(fmap.items()))

    @staticmethod
    def get_ranks(arr):
        """

        """
        sidx = np.argsort(arr, kind='mergesort')
        idx = np.concatenate(([0], np.flatnonzero(np.diff(arr[sidx]))+1, [arr.size]))
        inv_ranks = np.repeat(idx[:-1], np.diff(idx))[sidx.argsort()]
        return np.argsort(inv_ranks)[::-1]

    @staticmethod
    def get_histogram_edges_from_weight(wt):
        """

        """
        if wt <= 5:
            edges = np.linspace(0, wt, wt*2 +1)
        elif 5 < wt <= 10:
            edges = np.arange(0, wt+1, 1).astype(int)
        elif 10 < wt <= 20:
            edges = np.arange(0, wt+5, 5).astype(int)
        else:
            if (wt % 5 == 0):
                edges = np.arange(0, wt+5, 5).astype(int)
            else:
                edges = np.arange(0, wt+10, 10).astype(int)
        return edges

    def get_histogram(self, arr, edges):
        """

        """
        if self.bias == 'left':
            counts, edges = np.histogram(arr, edges)
        else:
            counts = np.zeros(len(edges) - 1, dtype=int)
            for idx, val in zip(*np.unique(np.searchsorted(edges, arr, side='left'), return_counts=True)):
                counts[idx - 1] = val
        return counts, edges

    def initialize_identifiers(self, raw_data, name_index=None, id_index=None, email_index=None):
        """

        """
        identifiers = dict()
        for key, i in zip(('name', 'id number', 'email'), (name_index, id_index, email_index)):
            if isinstance(i, int):
                identifiers[key] = raw_data[1:, i]
            elif i is not None:
                raise ValueError("invalid type(index): {}".format(type(i)))
        if len(identifiers) == 0:
            raise ValueError("input at least one: 'name_index', 'id_index', 'email_index'")
        self._identifiers.update(identifiers)

    def initialize_weighted_points(self, raw_data, homework_index=None, exam_index=None, extra_credit_index=None, homework_weight=None, exam_weight=None, extra_credit_weight=None):
        """

        """
        if all(i is None for i in (homework_index, exam_index, extra_credit_index)):
            raise ValueError("input at least one: 'homework_index', 'exam_index', 'extra_credit_index'")
        total_weight = 0
        for key, i, weight in zip(('homework', 'exam', 'extra credit'), (homework_index, exam_index, extra_credit_index), (homework_weight, exam_weight, extra_credit_weight)):
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
                header = raw_data[0, i]
                scores = raw_data[1:, i].astype(float)
                statistics = self.get_statistics(scores, axis=0)
                total_weight += np.nansum(wres)
                self._points[key] = {
                    'header' : header,
                    'score' : scores,
                    'weight' : wres,
                    'statistics' : statistics,
                    'total' : np.nansum(scores, axis=1)
                                        }
        return total_weight

    def initialize_grading_criteria(self, total_weight, fail_score=None, ace_score=None, decimals=None):
        """

        """
        ## get fail/ace scores
        if ace_score is None:
            ace_score = 0.95 * total_weight
        if fail_score is None:
            fail_score = ace_score / 2
        if fail_score >= ace_score:
            raise ValueError("fail_score ({}) must be less than ace_score ({})".format(fail_score, ace_score))
        ## get bin-edges for grades between ace and fail
        middle_edges = np.linspace(fail_score, ace_score, self.letters.size-1)
        edges = np.array([-1] + middle_edges.tolist() + [total_weight * 10])
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
            'weight' : total_weight,
            'fail' : fail_score,
            'ace' : ace_score,
            'edges' : edges,
            'message' : msg
                                        })

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
                'total' : tally
                                        }

    def get_grades(self, scores):
        """

        """
        indices = np.searchsorted(self.grading_criteria['edges'], scores, side=self.bias) - 1
        return self.letters[indices]

    def initialize_grade_points(self):
        """

        """
        ## homework + exam + extra credit + curve
        point_scores = np.nansum([value['total'] for key, value in self.points.items()], axis=0)
        ## grade
        self._final['score'] = point_scores
        self._final['grade'] = self.get_grades(point_scores)
        self._final['statistics'] = self.get_statistics(point_scores, axis=None)

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

    def initialize_students(self, ranks):
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
                            'score' : self.points[key]['score'][i, j]
                                                }
                pts[key] = assignment
            ## grade-points
            final = OrderedDict()
            for key in ('score', 'grade'):
                final[key] = self.final[key][i]
            pts['final'] = final
            ## class-wide ranking
            rank = {
                'numeric' : ranks[i],
                'message' : '{}/{}'.format(ranks[i], self.number_of_students)
                    }
            ## initialize student
            student = Student(identifiers, pts, rank)
            self._students.append(student)
        self._students = np.array(self._students)
