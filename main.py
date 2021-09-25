from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
import math


Window.size = (300, 400)
Window.minimum_width, Window.minimum_height = Window.size

# żeby self.result_int przejmował działania i można było się do nich odnieść
# żeby na wyświetlaczu pomiędzy składnikami operacji wyświetlana była spacja
# gdzie można - pozbyć się result_int, pobierać wartość dla result_txt prosto z temp
# w miejscach 'str(self.temp)' usunąć str bo self.temp to zawsze tekst
# napisać funkcję która w self.temp sprawdzi czy są dwa operatory obok siebie i nie doda kolejnego
# warunki napisać wszędzie w tej samej kolejności

class MainWidget(BoxLayout):
    operators = ["+", "-", "*", "/"]
    temp = "0"
    result_int = 0
    result_txt = StringProperty("0")

    def check_string_for_operator(self, string):
        # iterates through STRING starting from the end
        # checks if there is any operator '+', '-', '*', or '/'
        # if yes - returns most-right operator position for positive numbers
        # if not - returns False
        operator_pos = 0
        operator_found = False
        for i in string[-1::-1]:
            operator_pos -= 1
            if i in self.operators:
                operator_found = True
                break
        if bool(operator_found) == True:
            if operator_pos == -(len(string)):
                return False
            else:
                return operator_pos
        else:
            return False

    def check_string_for_double_operator(self, string):
        # checks if there are two operator signs close to each other
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
        # iterates through self.temp starting from the end
        # checks if there is any dot "."
        # if yes - returns most-right dot position
        # if not - returns False
        dot_pos = 0
        for i in string[-1::-1]:
            dot_pos -= 1
            if i == ".":
                return dot_pos
        else:
            return False

    def check_string_for_zeros_at_the_end(self, string):
        # if selt.temp is float type, iterates through starting from the end
        # checks if the number can be shortened from 'X.0' to 'X'
        # if yes - returns True
        # in not - returns False
        operator_pos = self.check_string_for_operator(string)
        dot_pos = self.check_string_for_dot(string)
        if operator_pos < -1:
            if dot_pos:
                if dot_pos < operator_pos:
                    return False
                else:
                    if dot_pos == -1:
                        # example '1+2.'
                        return False
                    else:
                        # example '1+2.00'
                        temporary = int(string[dot_pos + 1 :])
                        if temporary == 0:
                            return True
                        else:
                            return False
            else:
                return False
        else:
            if string.startswith("0"):
                # starts with 0
                # example '0.xxx'
                if string.endswith("+"):
                    # example '0.05+'
                    if eval(string[:-1]) == 0:
                        # if self.temp[:-1] converted to number == 0
                        return True
                    else:
                        # if self.temp[:-1] converted to number != 0
                        return False
                else:
                    # doesnt end with '+'
                    # example '0.050'
                    if eval(string) == 0:
                        # if self.temp converted to number == 0
                        return True
                    else:
                        # if self.temp converted to number != 0
                        return False
            else:
                # starts with number != 0
                # example '1.xxx'
                if string.endswith("+"):
                    # example '1.xx+'
                    if dot_pos < -2:
                        zeros_count = int(f"{-(dot_pos+2)}")
                        multiplier = int("1" + int(zeros_count) * "0")
                        multiplied = int(string[:dot_pos]) * multiplier
                        if str(string[:-1].replace('.', "")) == str(multiplied):
                            return True
                        else:
                            return False
                else:
                    # example '1.xxx'
                    if dot_pos < -1:
                        zeros_count = int(f"{-(dot_pos + 1)}")
                        multiplier = int("1" + int(zeros_count) * "0")
                        multiplied = int(string[:dot_pos]) * multiplier
                        if str(string.replace('.', "")) == str(multiplied):
                            return True
                        else:
                            return False

    def call_number(self, number):
        # calls number '0,1,2,3,4,5,6,7,8,9' for self.temp
        if self.temp != "0" and number == "0":
            self.temp = self.temp + number
            self.result_txt = self.temp.replace(".", ",")
        else:
            if self.temp == "0":
                self.temp = number
                self.result_txt = self.temp.replace(".", ",")
            else:
                self.temp = self.temp + number
                self.result_txt = self.temp.replace(".", ",")

# naprawić, nie działa przy '1+0.0' --> '1.0'
    def call_operation(self, operation_symbol):
        # calls operation '+ - * or /' for self.temp
        operator = operation_symbol
        operator_pos = self.check_string_for_operator(self.temp)
        dot_pos = self.check_string_for_dot(self.temp)
        zeros_after_dot = self.check_string_for_zeros_at_the_end(self.temp)
        if bool(operator_pos) == False:
            # no operator
            if bool(dot_pos) == False:
                # no dot, example '1' -> '1+'
                self.temp = self.temp + operator
                self.result_txt = self.temp
            else:
                # found dot
                if dot_pos == -1:
                    # dot at the end, example '1.' -> '1+'
                    self.temp = self.temp[:-1] + operator
                    self.result_txt = self.temp
                else:
                    # dot in the middle
                    if bool(zeros_after_dot) == True:
                        # example '1.00' -> '1+'
                        self.temp = self.temp[:dot_pos] + operator
                        self.result_txt = self.temp
                    else:
                        if self.temp.endswith("0"):
                            # example '1.050' -> '1.05+'
                            last_zero_pos = 0
                            for i in self.temp[-1::-1]:
                                if i == "0":
                                    last_zero_pos -= 1
                                else:
                                    break
                            self.temp = self.temp[:last_zero_pos] + operator
                            self.result_txt = self.temp.replace(".", ",")
                        else:
                            # example '1.05' -> '1.05+'
                            self.temp = self.temp + operator
                            self.result_txt = self.temp.replace(".", ",")
        else:
            # found operator
            if bool(dot_pos) == False:
                # no dot
                if operator_pos == -1:
                    # operator at the end
                    if self.temp[-1] == operator:
                        # example '1+' -> pass
                        pass
                    else:
                        # different operator exchange, example '1-' -> '1+'
                        self.temp = self.temp[:-1] + operator
                        self.result_txt = self.temp
                else:
                    # operator in the middle, example '1+1'
                    self.temp = str(eval(self.temp)) + operator
                    self.result_txt = self.temp
            else:
                # operator + dot
                if operator_pos == -1:
                    # operator at the end
                    if self.temp[-1] == operator:
                        # example '1.05+' -> pass
                        pass
                    else:
                        # different operator exchange, example '1-' -> '1+'
                        self.temp = self.temp[:-1] + operator
                        self.result_txt = self.temp.replace(".", ",")
                else:
                    # operator in the middle
                    self.temp = str(eval(self.temp)) + operator
                    self.result_txt = str(self.temp).replace(".", ",")

# napisać kod
    def button_percent(self):
        pass

    def button_plus_minus(self):
        operator_pos = self.check_string_for_operator(self.temp)
        dot_pos = self.check_string_for_dot(self.temp)
        two_close_operators = self.check_string_for_double_operator(self.temp)
        if bool(two_close_operators) == True:
            pass
        else:
            # check for operator
            if self.temp != "0":
                if bool(operator_pos) == False and self.temp != "0":
                    # no operator
                    if bool(dot_pos) == False:
                        # no dot, example '10' or '-10'
                        self.result_txt = str(-1 * int(self.temp))
                        self.temp = str(self.result_txt)
                    elif dot_pos == -1 and not "." in self.temp[:-1]:
                        # dot at the end, example '10.' or '-10.'
                        self.result_txt = str(-1 * int(self.temp[:-1])) + ","
                        self.temp = str(-1 * int(self.temp[:-1])) + "."
                    else:
                        # dot in the middle, example '1.05' or '-1.05'
                        # split to '1' and '.05'
                        # multiplicate '1' by -1 and concatenate '-1' + '.05'
                        # result '-1.05'
                        self.result_int = -1 * int(self.temp[:dot_pos])
                        if self.result_int == 0 and self.temp.startswith("0"):
                            # for example '0.05' can't do '0 * -1' so add '-' to the beginning and concatenate '-' + '0' + '.05'
                            # result '-0.05'
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
                            # for example '1.05'
                            self.result_txt = str(
                                self.result_int) + self.temp[dot_pos:].replace(".", ",")
                            self.temp = str(self.result_int) + \
                                self.temp[dot_pos:]
                else:
                    # operator found
                    if bool(dot_pos) == False:
                        # no dot
                        if operator_pos == -1:
                            # operator at the end, example '10+' or '-10+'
                            self.result_txt = f"{self.temp}neg({self.temp[:-1]})"
                            self.temp = f"{self.temp}({-1 * int(self.temp[:-1])})"
                        else:
                            # operator in the middle, example '10+10' or '-10+10'
                            self.result_txt = f"{self.temp[:operator_pos + 1]}{str(-1 * int(self.temp[operator_pos + 1:]))}"
                            self.temp = f"{self.temp[:operator_pos + 1]}{str(-1 * int(self.temp[operator_pos + 1:]))}"
                    else:
                        # dot found
                        if operator_pos == -1:
                            # operator at the end, dot in the middle, example '10.5+' or '-10.5+'
                            self.result_txt = f"{self.temp.replace('.',',')}neg({self.temp[:-1].replace('.',',')})"
                            if self.temp.startswith("-"):
                                self.temp = f"{self.temp}({self.temp[1:-1]})"
                            else:
                                self.temp = f"{self.temp}(-{self.temp[:-1]})"
                        else:
                            # operator in the middle, float numbers
                            self.result_txt = f"{self.temp[:operator_pos + 1].replace('.',',')}-{self.temp[operator_pos + 1:].replace('.',',')}"
                            self.temp = self.result_txt.replace(",", ".")

    def button_c(self):
        self.result_int = 0
        self.result_txt = "0"
        self.temp = "0"

# naprawić, usuwa cyfry z wyniku
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

# naprawić, nie działa temp z operatorem
    def button_one_divided_by(self):
        if self.temp == 0 or self.temp == "0" or self.temp == "0.0":
            self.result_txt = "Can't divide by 0!"

        else:
            self.result_int = 1 / float(self.temp)
            self.result_txt = str(self.result_int).replace(".", ",")
            self.temp = str(self.result_int)

# naprawić
    def button_exponentation(self):
        if self.temp != 0 and self.temp != "0":
            self.result_int = float(self.temp) ** 2
            self.result_txt = str(self.result_int).replace(".", ",")
            self.temp = str(self.result_int)
        else:
            self.temp = "0"

# naprawić, nie działa przy '1+2'
    def button_square_root(self):
        if float(self.temp) >= 0:
            self.result_int = math.sqrt(float(self.temp))
            if len(str(self.result_int)) > 3:
                str_sqrt_result = f"{self.result_int:.12f}"
                self.result_txt = str_sqrt_result.replace(".", ",")
                self.temp = str(self.result_int)
            else:
                self.result_txt = str(self.result_int).replace(".", ",")
                self.temp = str(self.result_int)
        else:
            pass

    def button_000(self):
        operator_pos = self.check_string_for_operator(self.temp)
        if self.temp != "0" and operator_pos != -1:
            self.temp = str(self.temp) + "000"
            self.result_txt = str(self.temp).replace(".", ",")

# naprawić ?
# dopisać dot_pos
    def button_coma(self):
        if "." not in str(self.temp):
            if str(self.temp)[-1] in self.operators:
                self.temp = str(self.temp) + "0."
                self.result_txt = str(self.temp).replace(".", ",")
            else:
                self.temp = str(self.temp) + "."
                self.result_txt = str(self.temp).replace(".", ",")
        else:
            if "." == str(self.temp)[-1]:
                pass
            else:
                counter_temp_characters = 0
                for i in str(self.temp)[-1::-1]:
                    counter_temp_characters += 1
                    if i in self.operators:
                        if i == str(self.temp)[-1]:
                            self.temp = str(self.temp) + "0."
                            self.result_txt = str(self.temp).replace(".", ",")
                        elif "." in str(self.temp)[-counter_temp_characters + 1:]:
                            pass
                        else:
                            self.temp = str(self.temp) + "."
                            self.result_txt = str(self.temp).replace(".", ",")

# -----------------NAPRAWIĆ------------------------------------------------------------------------------------------
# zrobić by klikając powtarzało ostatnią operację i aktualizowało temp
# błąd przy '10+2,'
# pokazuje wynik '0,0'
# pozwala dopisywać liczby do wyniku, edytować self.int ... ?
    def button_equals(self):
        operator_pos = self.check_string_for_operator(self.temp)
        dot_pos = self.check_string_for_dot(self.temp)
        zeros_after_dot = self.check_string_for_zeros_at_the_end(self.temp)
        if self.temp != "0":
            if bool(operator_pos) == True:
                if bool(dot_pos) == True:
                    if bool(zeros_after_dot) == True:
                        print("oper+dot+.0")
                        try:
                            self.result_int = eval(self.temp[:dot_pos])
                            self.result_txt = str(self.result_int).replace(".", ",")
                            self.temp = str(self.result_int)
                        except:
                            print("exception...")
                    else: # example '1+2.05'
                        self.result_int = eval(self.temp)
                        self.temp = str(self.result_int)
                        self.result_txt = self.temp.replace(".", ",")
                else:
                    print("oper+NOdot")
                    # napisać żeby robiło operację na tempie do operatora
                    # spr czy operator na końcu
                    try:
                        self.result_int = eval(self.temp)
                        self.result_txt = str(
                            self.result_int).replace(".", ",")
                        self.temp = str(self.result_int)
                    except:
                        pass
            else:
                if str(eval(self.temp)).endswith(".0"):
                    self.result_int = eval(self.temp)
                    self.temp = str(self.result_int)[:-2]
                    self.result_txt = self.temp.replace(".", ",")
                else:
                    pass
        else:
            pass

    def button_addition(self):
        self.call_operation("+")

    def button_substraction(self):
        self.call_operation("-")

    def button_multiplication(self):
        self.call_operation("*")

    def button_division(self):
        self.call_operation("/")

    def button_0(self):
        self.call_number("0")

    def button_1(self):
        self.call_number("1")

    def button_2(self):
        self.call_number("2")

    def button_3(self):
        self.call_number("3")

    def button_4(self):
        self.call_number("4")

    def button_5(self):
        self.call_number("5")

    def button_6(self):
        self.call_number("6")

    def button_7(self):
        self.call_number("7")

    def button_8(self):
        self.call_number("8")

    def button_9(self):
        self.call_number("9")


class Calc(App):
    pass


Calc().run()
