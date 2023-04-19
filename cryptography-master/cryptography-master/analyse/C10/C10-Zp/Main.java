import java.math.BigInteger;
import java.util.Random;

public class Main {

    private static int n = 5000; // total people
    private static Agent[] agents;

    /**
     * Generates p and coeffs
     * 
     * p needs s :thinking:
     * 
     * @param k
     * @return
     */
    public static int[] generate(int k) {
        // we wanna generate a huge prime number
        // higher than 2^n so any polynomial algorithm cannot break our polynomial
        // this number is stored as the 0-th element of our returned array
        // the next elements are randomly generated numbers within 0 and this high prime
        // they represent the coefficients of the polynomial
        int[] gen = new int[k + 1];

        BigInteger bi = BigInteger.valueOf((long) (n + 1));
        while (!bi.isProbablePrime(100) && (bi.compareTo(BigInteger.valueOf((int) Math.pow(2, n))) == -1)) {
            bi = bi.add(BigInteger.ONE);
        }

        gen[0] = bi.intValue();

        Random rd = new Random();
        for (int i = 1; i < k + 1; i++) {
            gen[i] = rd.nextInt(gen[0]);
        }

        return gen;
    }

    /**
     * 
     * @param p
     * @param m
     */
    public static void distribute(Polynomial p, int m, int prime) {
        // allocates the right size of the agent array
        // creates each agent
        // tells each agent about his key :
        // the value of the polynomial evaluated at their index
        agents = new Agent[m];
        for (int i = 0; i < m; i++) {
            agents[i] = new Agent(i + 1, p.eval(i + 1,prime));
        }
    }

    /**
     * 
     * @param k
     * @param agents
     * @return
     */
    public static BigInteger coalition(int k, Agent[] agents,int prime) {
        if (agents.length < k + 1) {
            System.out.println("Not enough agents.");
            System.exit(0);
        }
        BigInteger Big_prime = BigInteger.valueOf(prime);

        BigInteger s = BigInteger.ZERO;
        for (int i = 1; i <= k + 1; i++) {
            System.out.println("Current coalition iteration : " + i);
            BigInteger numerator = BigInteger.ONE;
            BigInteger denominator = BigInteger.ONE;

            // Lagrange Formula
            for (int j = 1; j <= k + 1; j++) {
                if (j != i) {
                    numerator = numerator.multiply(BigInteger.valueOf(-j));
                    // if (numerator.signum() < 0 && numerator.compareTo(Big_prime.negate()) < 0){
                    //     numerator = numerator.mod(Big_prime);
                    //     numerator = numerator.subtract(Big_prime);
                    // }else if(numerator.compareTo(Big_prime) > 0){
                    //     numerator = numerator.mod(Big_prime); 
                    // }
                    // System.out.println("numerator: "+numerator);
                    denominator = denominator.multiply(BigInteger.valueOf((i - j)));
                    // denominator = denominator.mod(Big_prime);
                    // System.out.println("denominator: "+denominator);
                }
            }
            BigInteger i_term = agents[i - 1].getKey();
            i_term = i_term.multiply(numerator);
            i_term = i_term.divide(denominator).mod(Big_prime);
            s = s.add(i_term).mod(Big_prime);

        }

        return s;
    }

    public static void main(String[] args) {
        if (args.length != 3) {
            System.err.println("Argument error ! The program takes 3 number. number of agents, secret and number for the coalition");
            return;
        }

        try {
            n = Integer.parseInt(args[0]);
        } catch (NumberFormatException e) {
            System.err.println("The argument "+ args[0] + " must be a number !");
            return;
        }
        int s;
        try {
            s = Integer.parseInt(args[1]);
        } catch (NumberFormatException e) {
            System.err.println("The argument "+ args[1] + " must be a number !");
            return;
        }
        // k out of n required
        // regular integers it is 7
        int k;
        try {
            k = Integer.parseInt(args[2]);
        } catch (NumberFormatException e) {
            System.err.println("The argument "+ args[2] + " must be a number !");
            return;
        }
        

        int[] gen = generate(k); // We generate a random array of coefficients, and specify what the minimal
                                 // amount of people required to break the secret should be
        int prime = gen[0];
        System.out.println("prime : " + prime); // our high prime
        // defines the size of the finite corpse we are working with

        System.out.println("Generated Polynomial :");
        Polynomial p = new Polynomial(gen, s); // the gen array gives all the coefficients of the polynomial, except for
                                               // the constant coefficient which is our secret s.
        System.out.println(p);

        distribute(p, n,prime); // We share the partial information among the agents
        System.out.println("Values given to agents :");
        for (Agent agent : agents)
            System.out.println(agent);

        System.out.println("Coalition result : " + String.valueOf(coalition(k, agents,prime)));

    }
}
