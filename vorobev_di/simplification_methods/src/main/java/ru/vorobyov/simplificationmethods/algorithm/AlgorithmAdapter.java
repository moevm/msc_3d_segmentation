package ru.vorobyov.simplificationmethods.algorithm;

import ru.vorobyov.simplificationmethods.service.python.PythonService;

import java.util.Objects;

public class AlgorithmAdapter {
    public Algorithm getAlgorithm(String methodFlag, String algorithmParam){
        Algorithm algorithm = switch (AlgorithmTypes.getFromFlag(methodFlag)){
            case BASIC -> null;
            case GEOMETRIC -> getGeometricAlgorithm(algorithmParam);
            case ITERATIVE -> getIterativeAlgorithm();
        };

        if (Objects.isNull(algorithm))
            throw new IllegalArgumentException("Данный алгоритм ещё не реализован!");

        return algorithm;
    }

    private GeometricSimplification getGeometricAlgorithm(String algorithmParam){
        int divisionNum = Integer.parseInt(algorithmParam);
        return new GeometricSimplification(divisionNum);
    }

    private IterativeSimplification getIterativeAlgorithm(){
        return new IterativeSimplification(new PythonService());
    }
}
