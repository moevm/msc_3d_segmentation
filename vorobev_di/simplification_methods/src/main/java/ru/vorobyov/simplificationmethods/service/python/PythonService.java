package ru.vorobyov.simplificationmethods.service.python;

import ru.vorobyov.simplificationmethods.configuration.ApplicationConfiguration;
import ru.vorobyov.simplificationmethods.configuration.ConfigurationFields;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

public class PythonService {
    private final static String SCRIPT_INPUT_PATH =
            ApplicationConfiguration.getProperty(ConfigurationFields.SCRIPT_PYTHON_INPUT);
    private final static String SCRIPT_OUTPUT_PATH =
            ApplicationConfiguration.getProperty(ConfigurationFields.SCRIPT_PYTHON_OUTPUT);
    private final static ConfigurationFields PYTHON_METHOD =
            ConfigurationFields.SCRIPT_PYTHON_METHOD;

    public void parseInputModel() {
        parseScript(SCRIPT_INPUT_PATH);
    }

    public void parseOutputModel() {
        parseScript(SCRIPT_OUTPUT_PATH);
    }

    public void doPythonMethod(PythonMethods method){
        final String methodPath = ApplicationConfiguration.getMethodProperty(PYTHON_METHOD, method);
        parseScript(methodPath);
    }

    private void parseScript(String scriptPath){
        boolean isSuccess = true;

        try {
            isSuccess = processScript(scriptPath);
        } catch (IOException e) {
            System.out.println("Ошибка во время запуска считывания модели");
            System.exit(-1);
        }

        if (!isSuccess)
            System.exit(-1);
    }

    private boolean processScript(String scriptPath) throws IOException {
        boolean isSuccess = true;
        String s;

        String pythonScript = new File(scriptPath).getAbsolutePath();
        Process p = Runtime.getRuntime().exec("python " + pythonScript);

        BufferedReader stdInput = new BufferedReader(new
                InputStreamReader(p.getInputStream()));

        BufferedReader stdError = new BufferedReader(new
                InputStreamReader(p.getErrorStream()));

        while ((s = stdInput.readLine()) != null)
            if (s.contains("-")){
                System.out.println("Не удалось считать модель");
                isSuccess = false;
            }

        while ((s = stdError.readLine()) != null) {
            System.err.println(s);
            isSuccess = false;
        }

        return isSuccess;
    }

}
