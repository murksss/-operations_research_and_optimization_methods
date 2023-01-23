from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from pulp import LpProblem, LpMaximize, LpVariable, LpConstraint, LpConstraintGE, LpConstraintLE
import pulp as p


class MatplotlibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("mainUi.ui", self)
        self.optimizeButton.clicked.connect(self.optimize)

    def optimize(self):

        try:
            u1min = float(self.u1Min.text())
            u1max = float(self.u1Max.text())
            u2min = float(self.u2Min.text())
            u2max = float(self.u2Max.text())
            x3min = float(self.x3Min.text())
            x3max = float(self.x3Max.text())
            x4min = float(self.x4Min.text())
            x4max = float(self.x4Max.text())
            x5min = float(self.x5Min.text())
            x5max = float(self.x5Max.text())
            ageIn = float(self.ageIn.text())
            sexIn = float(self.sexIn.text())
            x3In = float(self.x3In.text())
            x4In = float(self.x4In.text())
            x5In = float(self.x5In.text())
        except Exception as e:
            self.resultLabel.setText('Упс.. Проблема з введеними даними.')
            print(e)
            return 0
        if ageIn < 5 or ageIn > 11:
            self.resultLabel.setText('Дослідження проводилися на дітях віком від 5 до 11 років. Вкажіть корректний вік пацієнта')
            return 0
        elif sexIn < 1 or sexIn > 2:
            self.resultLabel.setText('Невірно вказана стать.')
            return 0
        elif x3In < x3min or x3In > x3max:
            self.resultLabel.setText('Невірно вказане значення "Об\'єм форсованого видиху".')
            return 0
        elif x4In < x4min or x4In > x4max:
            self.resultLabel.setText('Невірно вказане значення "Життєва ємність легень".')
            return 0
        elif x5In < x5min or x5In > x5max:
            self.resultLabel.setText('Невірно вказане значення "Максимальне значення потоку за першу секунду видиху".')
            return 0
        try:

            result = LpProblem('max_optimization', LpMaximize)
            u1 = LpVariable("u1", lowBound=u1min, upBound=u1max)
            u2 = LpVariable("u2", lowBound=u2min, upBound=u2max)
            result += 0.0014 * u1 * ageIn - 0.0214 * u2 * sexIn - 0.0147 * u2 * x4In + 0.0002 * u2 * x5In + \
                      0.0941 * sexIn + 0.5858 * x3In + 0.4046 * x4In - 0.0006 * x5In + 0.0485
            result += LpConstraint(0.0014 * u1 * ageIn - 0.0214 * u2 * sexIn - 0.0147 * u2 * x4In + 0.0002 * u2 * x5In + \
                      0.0941 * sexIn + 0.5858 * x3In + 0.4046 * x4In - 0.0006 * x5In + 0.0485 - x3min,
                                   LpConstraintGE, x3min), 'f1'
            result += LpConstraint(0.0014 * u1 * ageIn - 0.0214 * u2 * sexIn - 0.0147 * u2 * x4In + 0.0002 * u2 * x5In + \
                      0.0941 * sexIn + 0.5858 * x3In + 0.4046 * x4In - 0.0006 * x5In + 0.0485 - x3max,
                                   LpConstraintLE, x3max), 'f2'
            result += LpConstraint(
                0.0292 * u1 * x3In - 0.0002 * u1 * x5In - 0.0040 * ageIn - 0.1490 * x3In + 1.0604 * x4In + 0.0750 - x4min,
                LpConstraintGE, x4min), "a1"
            result += LpConstraint(
                0.0292 * u1 * x3In - 0.0002 * u1 * x5In - 0.0040 * ageIn - 0.1490 * x3In + 1.0604 * x4In + 0.0750 - x4max,
                LpConstraintLE, x4max), "a2"

            result += LpConstraint(
                8.1743 * u2 * x3In - 0.0554 * u2 * x5In - 15.0590 * sexIn - 32.2389 * x3In + 22.4936 * x4In + 0.9966 * x5In + 54.4474 - x5min,
                LpConstraintGE, x5min), "b1"
            result += LpConstraint(
                8.1743 * u2 * x3In - 0.0554 * u2 * x5In - 15.0590 * sexIn - 32.2389 * x3In + 22.4936 * x4In + 0.9966 * x5In + 54.4474 - x5max,
                LpConstraintLE, x5max), "b2"
            status = result.solve()
            u1 = p.value(u1)
            u2 = p.value(u2)
            x4out = round(0.0264 * u1 * x3In - 0.0001 * u1 * x5In - 0.0038 * ageIn - 0.1197 * x3In + 1.0391 * x4In + 0.0727, 2)
            x5out = round(7.608 * u2 * x3In - 0.0516 * u2 * x5In - 14.6938 * sexIn - 29.7786 * x3In + 21.6358 * x4In + 0.9885 * x5In + 53.5752, 2)

            x3model = round(0.0941 * sexIn + 0.5858 * x3In + 0.4046 * x4In - 0.0006 * x5In + 0.0485, 7)
            x3modelU1 = round(0.0014 * ageIn, 7)
            x3modelU2 = round(0.0214 * -sexIn - 0.0147 * x4In + 0.0002 * x5In, 7)
            x4model = round(0.0038 * -ageIn - 0.1197 * x3In + 1.0391 * x4In + 0.0727, 7)
            x4modelU = round(0.0264 * x3In - 0.0001 * x5In, 7)
            x5model = round(14.6938 * -sexIn - 29.7786 * x3In + 21.6358 * x4In + 0.9885 * x5In + 53.5752, 7)
            x5modelU = round(7.608 * x3In - 0.0516 * x5In, 7)

            if p.value(result.objective) < x3min or p.value(result.objective) > x3max \
                or x4out < x4min or x4out > x4max \
                or x5out < x5min or x5out > x5max \
                or u1 < u1min or u1 > u1max \
                or u2 < u2min or u2 > u2max:
                self.resultLabel.setText("Помилка обрахунків.")
            else:
                txt_res = f'Дозування препаратом Budesonide: {p.value(u1)} мг\n' \
                          f'Дозування препаратом Nedochromil: {p.value(u2)} мг\n' \
                          f"Об'єм форсованого видиху після лікуваня: {round(p.value(result.objective), 3)} л\n" \
                          f"Життєва ємність легень: {x4out} л\n" \
                          f"Максимальне значення потоку: {x5out} мл\n" \
                          f"Модель об`єму форс. видиху:\n \t\t\t{x3model} + ({x3modelU1})u1 + ({x3modelU2})u2\n" \
                          f"Модель ЖЄЛ:\n\t\t\t {x4model} + ({x4modelU})u1\n" \
                          f"Модель макс. знач. потоку:\n\t\t\t {x5model} + \t\t({x5modelU})u2\n"
                self.resultLabel.setText(txt_res)
        except Exception as e:
            self.resultLabel.setText(str(e))
            return 0


app = QApplication([])
app.setStyle('Fusion')
window = MatplotlibWidget()
window.setWindowTitle('Курсова робота Шкепаст Марко БС-93 ')
window.show()
app.exec_()
