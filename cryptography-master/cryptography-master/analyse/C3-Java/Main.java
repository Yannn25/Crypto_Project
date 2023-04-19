import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.Normalizer;
import java.text.Normalizer.Form;
import java.util.Random;
import java.util.Scanner;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Main class
 * 
 * @author Nico
 */
public class Main {

    /**
     * Generates a key
     * 
     * @return the key
     */
    public static Key G() {
        return new Key();
    }

    /**
     * Cyphers a message with the key
     * 
     * @param m the message
     * @param k the key
     * @return the cyphered message
     */
    public static Message E(Message m, Key k) {
        byte[][] cyphered = new byte[m.getBytes().length][2];
        for (int i = 0; i < m.getBytes().length; i++) {
            cyphered[i][0] = Utils.xor(m.getBytes()[i][0], k.getK()[i % 4][0]);
            cyphered[i][1] = Utils.xor(m.getBytes()[i][1], k.getK()[i % 4][1]);
        }

        return new Message(cyphered);
    }

    /**
     * Deciphers a cyphered message
     * 
     * @param m the cyphered message
     * @param k the key
     * @return the deciphered message
     */
    public static Message D(Message m, Key k) {
        return E(m, k);
    }

    /**
     * Executes exercice 1
     */
    public static void ex1() {
        System.out.println("==========EXERCICE 1==========");
        System.out.println("Generated key :");
        Key key = G();
        key.print();

        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a word : ");
        Message m = new Message(sc.nextLine());

        System.out.println("Your message in double byte format : ");
        m.printByteMessage();

        Message c = E(m, key);

        System.out.println("The cyphered message in double byte format : ");
        c.printByteMessage();

        System.out.println("The cyphered message : ");
        c.printMessage();

        Message d = D(c, key);
        System.out.println("The deciphered message in double byte format :");
        d.printByteMessage();

        System.out.println("The deciphered message :");
        d.printMessage();

        sc.close();
    }

    /**
     * Réponse Question 2 : En supposant que le texte est dans une certaine langue
     * (exemple anglais) et en connaissant l'algorithme de chiffrement ainsi que la
     * longueur de la clé, on peut trouver la clé en effectuant une analyse
     * fréquentielle sur le texte en question.
     * On créera 4 tables de fréquences pour le chiffrement modulo 4 et on
     * considèrera la lettre la plus fréquente de chaque table comme la lettre la
     * plus fréquente de la langue.
     * 
     * Un version améliorée prendre plus d'une lettre dans les lettre les plus
     * fréquentes.
     */
    public static void ex3() {
        System.out.println("==========EXERCICE 3==========");
        // Read the text (file or manual input)
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a path to a raw file :");
        String T = sc.nextLine();

        // We read the file and stock it in T if it exists
        try {
            Path path = Paths.get(T);
            if (Files.exists(path)) {
                Stream<String> lines = Files.lines(path);
                T = lines.collect(Collectors.joining("\n"));
                lines.close();

                // Normalization : We remove spaces, accents and turn all the characters into
                // upper case.
                T = Normalizer.normalize(T, Form.NFD);
                T = T.replaceAll("[^\\p{ASCII}]", "");
                T = T.replaceAll("\\W", "");
                T = T.toUpperCase();

                System.out.println("Text's length :" + String.valueOf(T.length()));
            } else {
                System.err.println("The argument must be a path !");
                sc.close();
                System.exit(1);
            }
        } catch (Exception e) {
            e.printStackTrace();
            sc.close();
            System.exit(1);
        } finally {
            sc.close();
        }

        // Minimal text length on which our analysis works
        System.out.println("Processing...");
        Random rd = new Random();
        int length = T.length();
        while (length != 0) {
            int positive = 0;
            for (int k = 0; k < 100; k++) {
                // Choose a start index randomly
                int startIndex = 0;
                if (length != T.length()) {
                    startIndex = rd.nextInt(T.length() - length);
                }
                // Get the substring from startIndex
                String substring = T.substring(startIndex, startIndex + length);
                // Encrypt the substring
                Message mess = E(new Message(substring), new Key());
                String cyphered = mess.getMessage();

                // Make the frequency tables
                FreqTable freq = new FreqTable();
                for (int i = 0; i < cyphered.length(); i++) {
                    freq.add(i % 4, cyphered.charAt(i));
                }
                // Get the most frequent letter in each table : we associate it with E because
                // we suppose that the text is in English (or French or Latin)
                char[] mostFreq = new char[4];
                mostFreq = freq.getMaxFreq();
                byte[][] b1 = Utils.toDoubleByte("E");

                byte[][] crackedKey = new byte[4][2];

                for (int i = 0; i < mostFreq.length; i++) {
                    byte[][] b2 = Utils.toDoubleByte("" + mostFreq[i]);
                    crackedKey[i][0] = Utils.xor(b1[0][0], b2[0][0]);
                    crackedKey[i][1] = Utils.xor(b1[0][1], b2[0][1]);
                }

                Key key = new Key(crackedKey);
                Message decyphered = D(new Message(cyphered), key);
                if (decyphered.getMessage().equals(substring)) {
                    positive++;
                }
            }

            if (positive >= 50) {
                length--;
                positive = 0;
            } else {
                System.out.println("Minimal length :" + length + 1);
                break;
            }
        }
    }

    /**
     * Display valid arguments
     */
    public static void printArgs() {
        System.out.println("Valid arguments :");
        System.out.println("\t--ex1");
        System.out.println("\t--ex3");
        System.out.println("\t--all");
    }

    /**
     * Main
     * 
     * @param args
     */
    public static void main(String[] args) {
        if (args.length == 1) {
            if (args[0].equals("--ex1")) {
                ex1();
            } else if (args[0].equals("--ex3")) {
                ex3();
            } else if (args[0].equals("--all")) {
                ex1();
                ex3();
            } else {
                System.out.println("Invalid argument");
                printArgs();
            }
        } else {
            System.out.println("Missing argument");
            printArgs();
        }
    }
}
