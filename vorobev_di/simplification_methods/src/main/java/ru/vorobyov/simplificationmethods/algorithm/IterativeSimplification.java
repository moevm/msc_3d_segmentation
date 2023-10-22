package ru.vorobyov.simplificationmethods.algorithm;

import ru.vorobyov.simplificationmethods.service.python.PythonMethods;
import ru.vorobyov.simplificationmethods.service.python.PythonService;

import java.util.List;

public class IterativeSimplification implements Algorithm{
    private final PythonService pythonService;
    public IterativeSimplification(PythonService pythonService) {
        this.pythonService = pythonService;
    }

    @Override
    public void process() {
        pythonService.doPythonMethod(PythonMethods.ITERATIVE_METHOD);
    }

    @Deprecated
    public void oldProcess() throws NoSuchMethodException {
        throw new NoSuchMethodException();
        /*List<float[]> points = mongoService.getAllPoints(MongoModels.INPUT);

        float[] centralPoint = calculateCentralPoint(points);
        float[] tangentPlane = calculateTangentPlane(points, centralPoint);
        float[] local_approximation = getLocalApproximation(tangentPlane, centralPoint);*/
    }

    private float[] getLocalApproximation(float[] tangentPlane, float[] centralPoint){
        return new float[]{tangentPlane[0] * centralPoint[0], tangentPlane[1] * centralPoint[1], tangentPlane[2] * centralPoint[2]};
    }

    private float[] calculateCentralPoint(List<float[]> points){
        float sumX = 0.0f;
        float sumY = 0.0f;
        float sumZ = 0.0f;

        for (float[] vertex : points)
            if (vertex.length >= 3) {
                sumX += vertex[0];
                sumY += vertex[1];
                sumZ += vertex[2];
            }

        return new float[]
                {sumX / points.size(), sumY / points.size(), sumZ / points.size()};
    }

    public static float[] calculateTangentPlane(List<float[]> points, float[] centerPoint) {
        // Вычисление отклонений координат точек от центральной точки
        final int axesNum = 3;
        float[][] deviations = new float[points.size()][axesNum];
        for (int i = 0; i < points.size(); i++) {
            for (int j = 0; j < axesNum; j++) {
                deviations[i][j] = points.get(i)[j] - centerPoint[j];
            }
        }
        // Вычисление транспонированной матрицы отклонений
        float[][] deviationsTransposed = new float[deviations[0].length][deviations.length];
        for (int i = 0; i < deviations.length; i++) {
            for (int j = 0; j < deviations[0].length; j++) {
                deviationsTransposed[j][i] = deviations[i][j];
            }
        }

        // Вычисление матрицы ковариации
        float[][] covarianceMatrix = new float[deviations[0].length][deviations[0].length];
        for (int i = 0; i < deviationsTransposed.length; i++) {
            for (int j = 0; j < deviationsTransposed.length; j++) {
                float sum = 0;
                for (int k = 0; k < deviationsTransposed[0].length; k++) {
                    sum += deviationsTransposed[i][k] * deviationsTransposed[j][k];
                }
                covarianceMatrix[i][j] = sum / (deviationsTransposed[0].length - 1);
            }
        }

        // Вычисление собственных значений и собственных векторов матрицы ковариации
        float[] eigenvalues = new float[covarianceMatrix.length];
        float[][] eigenvectors = new float[covarianceMatrix.length][covarianceMatrix.length];
        for (int i = 0; i < covarianceMatrix.length; i++) {
            float[] row = covarianceMatrix[i];
            float[][] identity = new float[row.length][row.length];
            for (int j = 0; j < row.length; j++) {
                identity[j][j] = 1.0f;
            }

            float[][] a = new float[row.length][row.length];
            for (int j = 0; j < row.length; j++) {
                for (int k = 0; k < row.length; k++) {
                    a[j][k] = row[j] * row[k];
                }
            }

            float[][] b = new float[row.length][row.length];
            for (int j = 0; j < row.length; j++) {
                for (int k = 0; k < row.length; k++) {
                    b[j][k] = identity[j][k] - (2 * a[j][k]);
                }
            }

            float[][] c = new float[row.length][row.length];
            for (int j = 0; j < row.length; j++) {
                for (int k = 0; k < row.length; k++) {
                    c[j][k] = (b[j][k] * (1 / (float) Math.sqrt(eigenvalues[i])));
                }
            }

            for (int j = 0; j < eigenvectors.length; j++) {
                eigenvectors[j][i] = c[j][0];
            }
        }

        // Находим индекс максимального собственного значения
        int maxEigenvalueIndex = 0;
        for (int i = 1; i < eigenvalues.length; i++) {
            if (eigenvalues[i] > eigenvalues[maxEigenvalueIndex]) {
                maxEigenvalueIndex = i;
            }
        }

        // Получаем собственный вектор, соответствующий максимальному собственному значению
        float[] tangentVector = eigenvectors[maxEigenvalueIndex];

        // Коэффициенты аппроксимирующей плоскости
        float a = tangentVector[0];
        float b = tangentVector[1];
        float c = tangentVector[2];

        return new float[] {a, b, c};
    }
}
