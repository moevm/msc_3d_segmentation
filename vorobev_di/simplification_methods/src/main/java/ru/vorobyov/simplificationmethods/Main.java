package ru.vorobyov.simplificationmethods;

import ru.vorobyov.simplificationmethods.algorithm.Algorithm;
import ru.vorobyov.simplificationmethods.algorithm.AlgorithmAdapter;
import ru.vorobyov.simplificationmethods.service.python.PythonService;

import java.util.Objects;

public class Main {
    private static final PythonService pythonService = new PythonService();

    public static void main(String[] args) {
        if (args.length < 2)
            throw new IllegalArgumentException("Введено менее 2-х аргументов!");

        String methodFlag = args[0];
        String algorithmParam = args[1];
        boolean isInputParseNeeded = args.length > 2 && Objects.nonNull(args[2]) && args[2].equals("-y");

        process(methodFlag, algorithmParam, isInputParseNeeded);
    }

    static void process(String methodFlag, String algorithmParam, boolean isInputParseNeeded){
        if (isInputParseNeeded)
            readModel();
        processAlgorithm(methodFlag, algorithmParam);
        writeModel();
        System.exit(0);
    }

    static void processAlgorithm(String methodFlag, String algorithmParam){
        Algorithm algorithm = getAlgorithm(methodFlag, algorithmParam);
        long start = System.currentTimeMillis();

        algorithm.process();

        double elapsedTimeInSec = (System.currentTimeMillis() - start);

        System.out.println("Готово!");
        System.out.println("Затрачено времени в мс: " + elapsedTimeInSec);
    }

    static Algorithm getAlgorithm(String methodFlag, String algorithmParam){
        return new AlgorithmAdapter()
                .getAlgorithm(methodFlag, algorithmParam);
    }

    static void readModel(){
        pythonService.parseInputModel();
    }

    static void writeModel(){
        pythonService.parseOutputModel();
    }
}
