from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
import math


Window.size = (300, 400)
Window.minimum_width, Window.minimum_height = Window.size


class MainWidget(BoxLayout):
    operators = ["+", "-", "*", "/"]
    temp = "0"
    result_int = 0
    result_txt = StringProperty("0")

    def check_string_for_operator(self, string):
        operator_pos = 0
        operator_found = False
        for i in string[-1::-1]:
            operator_pos -= 1
            if i in self.operators:
                operator_found = True
                break
        if bool(operator_found):
            if operator_pos == -(len(string)):
                return False
            else:
                return operator_pos
        else:
            return False

    def check_string_for_double_operator(self, string):
        operator_pos = self.check_string_for_operator(string)
        operator_combinations = ["+-", "--", "*-", "/-"]
        if operator_pos != -1:
            for i in operator_combinations:
                if i in string:
                    return True
            else:
                return False
        else:
            return False

    def check_string_for_dot(self, string):
        dot_pos = 0
        for i in string[-1::-1]:
            dot_pos -= 1
            if i == ".":
                return dot_pos
        else:
            return False

    def check_string_for_zeros_at_the_end(self, string):
        operator_pos = self.check_string_for_operator(string)
        dot_pos = self.check_string_for_dot(string)
        if operator_pos < -1:
            if dot_pos:
                if dot_pos < operator_pos:
                    return False
                else:
                    if dot_pos == -1:
                        return False
                    else:
                        temporary = int(string[dot_pos + 1:])
                        if temporary == 0:
                            return True
                        else:
                            return False
            else:
                return False
        else:
            if string.startswith("0"):
                if string.endswith("+"):
                    if eval(string[:-1]) == 0:
                        return True
                    else:
                        return False
                else:
                    if eval(string) == 0:
                        return True
                    else:
                        return False
            else:
                if string.endswith("+"):
                    if dot_pos < -2:
                        zeros_count = int(f"{-(dot_pos+2)}")
                        multiplier = int("1" + int(zeros_count) * "0")
                        multiplied = int(string[:dot_pos]) * multiplier
                        if str(string[:-1].replace('.', "")) == str(multiplied):
                            return True
                        else:
                            return False
                else:
                    if dot_pos < -1:
                        zeros_count = int(f"{-(dot_pos + 1)}")
                        multiplier = int("1" + int(zeros_count) * "0")
                        multiplied = int(string[:dot_pos]) * multiplier
                        if str(string.replace('.', "")) == str(multiplied):
                            return True
                        else:
                            return False

    def call_number(self, number):
        operator_pos = self.check_string_for_operator(self.temp)
        if self.temp == "0":
            self.temp = number
            self.result_txt = self.temp.replace(".", ",")
        else:
            if number != "0":
                self.temp = self.temp + number
                self.result_txt = self.temp.replace(".", ",")
            else:
                if not operator_pos:
                    self.temp = self.temp + number
                    self.result_txt = self.temp.replace(".", ",")
                else:
                    if operator_pos == -2 and self.temp[-1] == "0":
                        pass
                    else:
                        self.temp = self.temp + number
                        self.result_txt = self.temp.replace(".", ",")

    def call_operation(self, operation_symbol):
        operator = operation_symbol
        operator_pos = self.check_string_for_operator(self.temp)
        dot_pos = self.check_string_for_dot(self.temp)
        zeros_after_dot = self.check_string_for_zeros_at_the_end(self.temp)
        if not bool(operator_pos):
            if not bool(dot_pos):
                self.temp = self.temp + operator
                self.result_txt = self.temp
            else:
                if dot_pos == -1:
                    self.temp = self.temp[:-1] + operator
                    self.result_txt = self.temp
                else:
                    if bool(zeros_after_dot):
                        self.temp = self.temp[:dot_pos] + operator
                        self.result_txt = self.temp
                    else:
                        if self.temp.endswith("0"):
                            last_zero_pos = 0
                            for i in self.temp[-1::-1]:
                                if i == "0":
                                    last_zero_pos -= 1
                                else:
                                    break
                            self.temp = self.temp[:last_zero_pos] + operator
                            self.result_txt = self.temp.replace(".", ",")
                        else:
                            self.temp = self.temp + operator
                            self.result_txt = self.temp.replace(".", ",")
        else:
            if not bool(dot_pos):
                if operator_pos == -1:
                    if self.temp[-1] == operator:
                        pass
                    else:
                        self.temp = self.temp[:-1] + operator
                        self.result_txt = self.temp
                else:
                    self.temp = str(eval(self.temp)) + operator
                    self.result_txt = self.temp
            else:
                if operator_pos == -1:
                    if self.temp[-1] == operator:
                        pass
                    else:
                        self.temp = self.temp[:-1] + operator
                        self.result_txt = self.temp.replace(".", ",")
                else:
                    self.temp = str(eval(self.temp)) + operator
                    self.result_txt = self.temp.replace(".", ",")

    def button_percent(self):
        operator_pos = self.check_string_for_operator(self.temp)
        dot_pos = self.check_string_for_dot(self.temp)
        if not bool(operator_pos):
            self.temp = "0"
            self.result_txt = "0"
        else:
            if bool(dot_pos):
                if operator_pos == -1:
                    self.temp = self.temp + \
                        str(eval(self.temp[:-1]) * 0.01)
                    self.result_txt = self.temp.replace(".", ",")
                else:
                    self.temp = self.temp[:operator_pos + 1] + str(
                        float(self.temp[operator_pos + 1:]) * 0.01 * float(self.temp[:operator_pos]))
                    self.result_txt = self.temp.replace(".", ",")
            else:
                if operator_pos == -1:
                    self.temp = self.temp + str(int(self.temp[:-1]) * 0.01)
                    self.result_txt = self.temp.replace(".", ",")
                else:
                    self.temp = self.temp[:operator_pos + 1] + str(
                        int(self.temp[operator_pos + 1:]) * 0.01 * int(self.temp[:operator_pos]))
                    self.result_txt = self.temp.replace(".", ",")

    def button_plus_minus(self):
        operator_pos = self.check_string_for_operator(self.temp)
        dot_pos = self.check_string_for_dot(self.temp)
        two_close_operators = self.check_string_for_double_operator(self.temp)
        if bool(two_close_operators):
            pass
        else:
            if self.temp != "0":
                if not bool(operator_pos) and self.temp != "0":
                    if not bool(dot_pos):
                        self.result_txt = str(-1 * int(self.temp))
                        self.temp = str(self.result_txt)
                    elif dot_pos == -1 and not "." in self.temp[:-1]:
                        self.result_txt = str(-1 * int(self.temp[:-1])) + ","
                        self.temp = str(-1 * int(self.temp[:-1])) + "."
                    else:
                        self.result_int = -1 * int(self.temp[:dot_pos])
                        if self.result_int == 0 and self.temp.startswith("0"):
                            if self.temp.startswith("-"):
                                self.result_txt = self.temp[:dot_pos] + \
                                    self.temp[dot_pos:].replace(".", ",")
                                self.temp = str(self.result_int) + \
                                    self.temp[dot_pos:]
                            else:
                                self.result_txt = "-" + \
                                    self.temp[:dot_pos] + \
                                    self.temp[dot_pos:].replace(".", ",")
                                self.temp = "-" + \
                                    str(self.result_int) + self.temp[dot_pos:]
                        else:
                            self.result_txt = str(
                                self.result_int) + self.temp[dot_pos:].replace(".", ",")
                            self.temp = str(self.result_int) + \
                                self.temp[dot_pos:]
                else:
                    if not bool(dot_pos):
                        if operator_pos == -1:
                            self.result_txt = f"{self.temp}neg({self.temp[:-1]})"
                            self.temp = f"{self.temp}({-1 * int(self.temp[:-1])})"
                        else:
                            self.result_txt = f"{self.temp[:operator_pos + 1]}{str(-1 * int(self.temp[operator_pos + 1:]))}"
                            self.temp = f"{self.temp[:operator_pos + 1]}{str(-1 * int(self.temp[operator_pos + 1:]))}"
                    else:
                        if operator_pos == -1:
                            self.result_txt = f"{self.temp.replace('.',',')}neg({self.temp[:-1].replace('.',',')})"
                            if self.temp.startswith("-"):
                                self.temp = f"{self.temp}({self.temp[1:-1]})"
                            else:
                                self.temp = f"{self.temp}(-{self.temp[:-1]})"
                        else:
                            self.result_txt = f"{self.temp[:operator_pos + 1].replace('.',',')}-{self.temp[operator_pos + 1:].replace('.',',')}"
                            self.temp = self.result_txt.replace(",", ".")

    def button_c(self):
        self.result_int = 0
        self.result_txt = "0"
        self.temp = "0"

    def button_backspace(self):
        if self.temp == 0 and self.temp == "0":
            pass
        elif len(str(self.temp)) > 1:
            self.temp = str(self.temp)[:-1]
            self.result_int = self.temp
            self.result_txt = str(self.result_int).replace(".", ",")
        else:
            self.result_int = 0
            self.result_txt = str(self.result_int).replace(".", ",")
            self.temp = "0"

    def button_one_divided_by(self):
        operator_pos = self.check_string_for_operator(self.temp)
        if bool(operator_pos):
            if operator_pos == -1:
                if eval(self.temp[:-1]) == 0:
                    self.result_txt = "Can't divide by 0!"
                else:
                    self.result_txt = self.temp.replace(
                        ".", ",") + "1/" + self.temp[:-1].replace(".", ",")
                    self.temp = self.temp + str(1 / eval(self.temp[:-1]))
            else:
                if eval(self.temp[operator_pos + 1:]) == 0:
                    self.result_txt = "Can't divide by 0!"
                else:
                    self.result_txt = self.temp[:operator_pos + 1].replace(
                        ".", ",") + "1/" + self.temp[operator_pos + 1:].replace(".", ",")
                    self.temp = self.temp[:operator_pos + 1] + \
                        str(1 / eval(self.temp[operator_pos + 1:]))
        else:
            if eval(self.temp) == 0:
                self.result_txt = "Can't divide by 0!"
            else:
                if bool(operator_pos):
                    pass
                else:
                    self.result_int = 1 / float(self.temp)
                    self.result_txt = str(self.result_int).replace(".", ",")
                    self.temp = str(self.result_int)

    def button_exponentation(self):
        operator_pos = self.check_string_for_operator(self.temp)
        if bool(operator_pos):
            if operator_pos == -1:
                if self.temp[:-1] == "0":
                    self.temp = "0+0"
                    self.result_txt = "0+sqr(0)"
                else:
                    self.result_txt = f"{self.temp.replace('.',',')}sqr({self.temp.replace('.',',')[:-1]})"
                    self.temp = f"{self.temp}{eval(self.temp[:-1]) ** 2}"
            else:
                self.result_txt = f"{self.temp.replace('.',',')[:operator_pos + 1]}sqr({self.temp.replace('.',',')[operator_pos + 1:]})"
                self.temp = f"{self.temp[:operator_pos + 1]}{eval(self.temp[operator_pos + 1:]) ** 2}"
        else:
            if self.temp != "0":
                self.result_int = eval(self.temp) ** 2
                self.result_txt = str(self.result_int).replace(".", ",")
                self.temp = str(self.result_int)
            else:
                self.temp = "0"

    def button_square_root(self):
        operator_pos = self.check_string_for_operator(self.temp)
        if self.temp.startswith("-") and bool(operator_pos) == False:
            self.result_txt = "Wrong data input!"
        elif self.temp.startswith("-") and operator_pos == -1:
            self.result_txt = "Wrong data input!"
        else:
            if bool(operator_pos):
                if operator_pos == -1:
                    self.result_txt = f"{self.temp.replace('.',',')}sqrt({self.temp[:-1].replace('.',',')})"
                    self.temp = self.temp + \
                        str(math.sqrt(eval(self.temp[:-1])))
                else:
                    self.result_txt = f"{self.temp[:operator_pos + 1].replace('.',',')}sqrt({self.temp[operator_pos + 1:].replace('.',',')})"
                    self.temp = self.temp[:operator_pos + 1] + str(math.sqrt(eval(self.temp[operator_pos + 1:])))
            else:
                self.result_int = math.sqrt(eval(self.temp))
                if len(str(self.result_int)) > 3:
                    str_sqrt_result = f"{self.result_int:.12f}"
                    self.result_txt = str_sqrt_result.replace(".", ",")
                    self.temp = str(self.result_int)
                else:
                    self.result_txt = str(self.result_int).replace(".", ",")
                    self.temp = str(self.result_int)

    def button_000(self):
        operator_pos = self.check_string_for_operator(self.temp)
        if self.temp == "0" or operator_pos == -1 or (operator_pos == -2 and self.temp[-1] == "0"):
            pass
        else:
            self.temp = str(self.temp) + "000"
            self.result_txt = str(self.temp).replace(".", ",")

    def button_coma(self):
        operator_pos = self.check_string_for_operator(self.temp)
        dot_pos = self.check_string_for_dot(self.temp)
        if bool(dot_pos):
            if dot_pos == -1 or "." in str(self.temp[operator_pos:]):
                pass
            elif operator_pos == -1:
                self.temp = str(self.temp) + "0."
                self.result_txt = str(self.temp).replace(".", ",")
            else:
                self.temp = str(self.temp) + "."
                self.result_txt = str(self.temp).replace(".", ",")
        else:
            if str(self.temp)[-1] in self.operators:
                self.temp = str(self.temp) + "0."
                self.result_txt = str(self.temp).replace(".", ",")
            else:
                self.temp = str(self.temp) + "."
                self.result_txt = str(self.temp).replace(".", ",")

    def button_equals(self):
        operator_pos = self.check_string_for_operator(self.temp)
        dot_pos = self.check_string_for_dot(self.temp)
        zeros_after_dot = self.check_string_for_zeros_at_the_end(self.temp)
        if self.temp != "0":
            if bool(operator_pos):
                if operator_pos == -1:
                    pass
                else:
                    if bool(dot_pos):
                        if bool(zeros_after_dot):
                            self.result_int = eval(self.temp[:dot_pos])
                            self.result_txt = str(self.result_int).replace(".", ",")
                            self.temp = "0"
                        else:
                            self.result_int = eval(self.temp)
                            self.temp = str(self.result_int)
                            self.result_txt = self.temp.replace(".", ",")
                            self.temp = "0"
                    else:
                        if operator_pos == -1:
                            self.result_txt = (self.temp + self.temp[:-1]).replace(".", ",")
                            self.temp = self.temp + self.temp[:-1]
                            self.result_int = eval(self.temp)
                            self.temp = "0"
                        else:
                            self.result_int = eval(self.temp)
                            self.result_txt = str(self.result_int).replace(".", ",")
                            self.temp = "0"
            else:
                if str(eval(self.temp)).endswith(".0"):
                    self.result_int = eval(self.temp)
                    self.temp = str(self.result_int)[:-2]
                    self.result_txt = self.temp.replace(".", ",")
                    self.temp = "0"


class Calc(App):
    pass


Calc().run()
