import java.util.HashMap;

/**
 * Class that represents the four frequency tables in order to crack the key
 * Each table is represent by a HashMap and are stocked in an ArrayList.
 * 
 * @author Nico
 */
public class FreqTable {
    // private ArrayList<HashMap<Character, Integer>> freq;
    private HashMap<Character, Integer> freq[];

    /**
     * Constructor
     */
    @SuppressWarnings("unchecked")
    public FreqTable() {
        freq = new HashMap[4];
        for (int i = 0; i < 4; i++) {
            freq[i] = new HashMap<Character, Integer>();
        }
    }

    /**
     * Increments the number associated with a character
     * Adds the key and the value 1 if the key doesn't exist.
     * 
     * @param tableIndex     the index in freq
     * @param tableCharIndex the key character
     */
    public void add(int tableIndex, char tableCharIndex) {
        int occ = freq[tableIndex].getOrDefault(tableCharIndex, 0);
        freq[tableIndex].put(tableCharIndex, occ + 1);
    }

    /**
     * Getter
     * 
     * @return the frequency tables
     */
    public HashMap<Character, Integer>[] getFreq() {
        return freq;
    }

    /**
     * Get the most frequent character in each table
     * 
     * @return an arraylist with the most frequent character in each table
     */
    public char[] getMaxFreq() {
        char[] mostFreq = new char[4];
        int count = 0;
        for (HashMap<Character, Integer> hm : freq) {
            char max = 0;
            int m = 0;

            for (char c : hm.keySet()) {
                if (hm.get(c) > m) {
                    max = c;
                    m = hm.get(c);
                }
            }
            mostFreq[count] = max;
            count++;
        }
        return mostFreq;
    }

}
