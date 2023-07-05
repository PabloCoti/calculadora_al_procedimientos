from PyQt5.QtWidgets import QMainWindow
from fractions import Fraction as FR
from PyQt5 import uic  # Lanza error, pero es por el pycharm, no porque no funcione
import utils

"""
Cadena de Markov (matrices de cualquier orden que sea válido)
"""

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar archivo .ui
        uic.loadUi("views/designs/main_view.ui", self)

        # Mostrar interfaz
        self.show()

        # Default actions
        self.stackedWidget.setCurrentIndex(0)
        self.frame_matrices_matrizb.hide()
        self.frame_encryption.hide()

        # User interactions
        self.pushButton_calcular.clicked.connect(self.calculate_result)
        self.spinBox_matrices_numeromatrices.valueChanged.connect(self.increase_shown_matrix)
        self.spinBox_matrices_numeromatrices.valueChanged.connect(self.increase_hidden_matrix)
        self.comboBox_calculator_mode.currentIndexChanged.connect(self.swap_mode)
        self.comboBox_matrix_ab_op.currentIndexChanged.connect(self.swap_mode)

    def swap_mode(self):
        if self.comboBox_calculator_mode.currentText() == 'Matrices':
            self.stackedWidget.setCurrentIndex(1)

        else:
            self.stackedWidget.setCurrentIndex(0)

        if self.comboBox_calculator_mode.currentText() == 'Encriptar':
            self.stackedWidget.setCurrentIndex(1)
            self.frame_encryption.show()
            self.spinBox_matrices_numeromatrices.hide()
            self.comboBox_matrix_a_op.hide()
            self.frame_matrices_matrizb.hide()
            self.groupBox_ma.setTitle('Contraseña')

        elif self.comboBox_calculator_mode.currentText() == 'Desencriptar':
            self.stackedWidget.setCurrentIndex(1)
            self.spinBox_matrices_numeromatrices.hide()
            self.comboBox_matrix_ab_op.hide()
            self.comboBox_matrix_a_op.hide()
            self.frame_matrices_matrizb.show()
            self.frame_encryption.show()
            self.lineEdit_e_message.clear()
            self.frame_matrices_matrizb.setTitle('Matriz encriptada')
            self.groupBox_ma.setTitle('Contraseña')

        else:
            self.frame_encryption.hide()
            self.spinBox_matrices_numeromatrices.show()
            self.comboBox_matrix_a_op.show()
            self.frame_matrices_matrizb.hide()
            self.groupBox_ma.setTitle('Matriz A')
            self.frame_matrices_matrizb.setTitle('Matriz B')

        if self.comboBox_matrix_ab_op.currentText() == 'Markov':
            self.frame_encryption.show()
            self.frame_matrices_matrizb.show()
            self.comboBox_matrix_a_op.hide()
            self.label_e_message.setText('Cantidad de ciclos')

        elif self.comboBox_matrix_ab_op.currentText() == '*' or self.comboBox_matrix_ab_op.currentText() == '+' or \
                self.comboBox_matrix_ab_op.currentText() == '-':
            self.frame_matrices_matrizb.show()
            self.comboBox_matrix_a_op.hide()


        else:
            self.frame_encryption.hide()
            self.label_e_message.setText('Mensaje')

    def calculate_matrix_result(self):
        a = utils.matrix_convertion(self.textEdit_ma.toPlainText())

        if self.frame_matrices_matrizb.isVisible():
            b = utils.matrix_convertion(self.textEdit_mb.toPlainText())

            operand = self.comboBox_matrix_ab_op.currentText()

            if operand == '*':
                m_result = utils.matrix_mult(a, b)

                self.update_matrix_results(m_result)

            elif operand == '+':
                m_result = utils.matrix_sum(a, b)

                self.update_matrix_results(m_result)

            elif operand == '-':
                m_result = utils.matrix_sub(a, b)

                self.update_matrix_results(m_result)

            elif operand == 'Markov':
                cicles = self.lineEdit_e_message.text()
                m_result = utils.markov_chain(a, b, cicles)

                self.update_matrix_results(m_result)

        if self.comboBox_matrix_a_op.isVisible():
            opt = self.comboBox_matrix_a_op.currentText()

            if opt == 'Traspuesta':
                m_result = utils.matrix_traspose(a)

                self.update_matrix_results(m_result)

            elif opt == 'Inversa':
                m_result = utils.matrix_invert(a)

                self.update_matrix_results(m_result)

            elif opt == 'Determinante':
                m_result = utils.matrix_determinant(a)

                self.update_matrix_results(m_result)

            elif opt == 'Rango':
                m_result = utils.matrix_range(a)

                self.update_matrix_results(m_result)

    def update_matrix_results(self, m_result):
        result = ''
        if isinstance(m_result, list):
            result += 'Fractions\n'
            for r in m_result:
                for n in r:
                    result += f"{FR(n).limit_denominator()}   "
                result += '\n'

            result += '\nDecimals\n'
            for r in m_result:
                for n in r:
                    result += f"{float(n)} "

                result += '\n'

            self.textBrowser_matrix_result.setText(result)

        else:
            self.textBrowser_matrix_result.setText(str(m_result))

    def increase_shown_matrix(self, value):
        if value == 2:
            self.frame_matrices_matrizb.show()
            self.comboBox_matrix_a_op.hide()

    def increase_hidden_matrix(self, value):
        if value == 1:
            self.frame_matrices_matrizb.hide()
            self.comboBox_matrix_a_op.show()

    def calculate_result(self):
        op_string = self.textEdit_input.toPlainText()
        mode = self.comboBox_calculator_mode.currentText()

        if mode == 'Normal':
            result = utils.parse_aritmethic(op_string)
            answer = f"{op_string}\n=\n{FR(result).limit_denominator()}"

            self.update_results(answer)

        elif mode == 'Sistema de Ecuaciones (Sustitución)':
            result = utils.equation_parse(op_string, 'Sustitución')
            answer = f"{op_string} \n=\n {result}"

            self.update_results(answer)

        elif mode == 'Sistema de Ecuaciones (Igualación)':
            result = utils.equation_parse(op_string, 'Igualación')
            answer = f"{op_string} \n=\n {result}"

            self.update_results(answer)

        elif mode == 'Sistema de Ecuaciones (Reducción)':
            result = utils.equation_parse(op_string, 'Reducción')
            answer = f"{op_string} \n=\n {result}"

            self.update_results(answer)

        elif mode == 'Sistema de Ecuaciones (Eliminación Gaussiana)':
            result = utils.equation_parse(op_string, 'Eliminación Gaussiana')
            answer = f"{op_string} \n=\n {result}"

            self.update_results(answer)

        elif mode == 'Sistema de Ecuaciones (Gauss Jordan)':
            result = utils.equation_parse(op_string, 'Gauss Jordan')
            answer = f"{op_string} \n=\n {result}"

            self.update_results(answer)

        elif mode == 'Números Complejos':
            result = utils.compound_parse(op_string)
            answer = f"{op_string} = {result}"

            self.update_results(answer)

        elif mode == 'Matrices':
            self.calculate_matrix_result()

        elif mode == 'Encriptar':
            message = self.lineEdit_e_message.text()
            key = self.textEdit_ma.toPlainText()

            self.lineEdit_e_message.setText(f"Matriz original:\n{utils.message_to_matrix(message)}")

            e_matrix = utils.encrypt_matrix(message, key)

            if e_matrix != 'Error':
                e_message = utils.matrix_to_message(e_matrix)
                print(e_message)
                self.lineEdit_e_message.setText(e_message)


            self.update_matrix_results(e_matrix)

        elif mode == 'Desencriptar':
            e_matrix = self.textEdit_mb.toPlainText()
            key = self.textEdit_ma.toPlainText()

            d_matrix = utils.decrypt_matrix(e_matrix, key)

            if e_matrix != 'Error':
                d_message = utils.matrix_to_message(d_matrix)
                print(d_message)
                self.lineEdit_e_message.setText(d_message)

            self.update_matrix_results(d_matrix)

        elif mode == 'Sistema de Ecuaciones (Sarrus)':
            result = utils.equation_parse(op_string, 'Sarrus')
            answer = f"{op_string} \n=\n {result}"

            self.update_results(answer)

    def update_results(self, string):
        self.textBrowser_result.append(string)
