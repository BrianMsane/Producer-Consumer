import java.util.List;
import java.util.ArrayList;

public class ITstudent {

    // member variables
    int ID;
    String name;
    String program;
    double average;
    char status;
    List<String> courses = new ArrayList<>();
    List<Double> marks = new ArrayList<>();

    public static void main(String args[]) {
        System.out.println("This is the student class");
    }

    public double computeAverage() {
        double total = 0;
        for (Double mark : this.marks) {
            total += mark;
        }
        return total;
    }
}
