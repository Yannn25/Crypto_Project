import java.util.Random;

/**
 * Class that represent a key
 * It is basically an array of 4 groups of 2 bytes.
 * 
 * @author Nico
 */
public class Key {
    private byte[][] K;

    /**
     * Constructor that generates a key
     */
    public Key() {
        Random r = new Random();
        K = new byte[4][2];
        for (int i = 0; i < K.length; i++) {
            r.nextBytes(K[i]);
        }
    }

    /**
     * Constructor that creates a key
     * used in cracking
     * 
     * @param K
     */
    public Key(byte[][] K) {
        this.K = K;
    }

    /**
     * Print function
     */
    public void print() {
        for (int i = 0; i < K.length; i++) {
            String s1 = String.format("%8s", Integer.toBinaryString(K[i][0] & 0xFF)).replace(' ', '0');
            String s2 = String.format("%8s", Integer.toBinaryString(K[i][1] & 0xFF)).replace(' ', '0');
            System.out.println("k" + String.valueOf(i) + ": " + s1 + " " + s2);
        }
    }

    /**
     * Getter
     * 
     * @return the key in byte array format
     */
    public byte[][] getK() {
        return K;
    }
}