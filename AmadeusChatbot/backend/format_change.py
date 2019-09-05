# formatchage for output athentic purpose
class format_change(object):
    def __init__(self,old_format):
        self.old = old_format

    def tostring(self):
        old_format = self.old
        # print(old_format)
        string = " knowledge_area : '{}'\n area_abstract : '{}'\n area_url : '{}'\n" \
                 " degree : '{}'\n course_number : '{}'\n course_name : '{}'\n course_uoc : '{}'\n course_url : '{}'\n " \
                 " course_outline : '{}'\n faculty : '{}'\n school : '{}'\n course_term : '{}'\n " \
                 " timetable_url : '{}'\n".format(old_format[0],old_format[1],old_format[2],old_format[3],
                                                  old_format[4],old_format[5],old_format[6],old_format[7],
                                                  old_format[8],old_format[9],old_format[10],old_format[11],old_format[12],)
        return string



if __name__ == '__main__':
    list = [1,2,3,4,5]
    a = format_change(list)
    a.tostring()