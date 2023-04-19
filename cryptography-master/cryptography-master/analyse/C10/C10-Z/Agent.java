import java.math.BigInteger;

public class Agent {
    private final int id;
    private final BigInteger key;

    /**
     * An agent has an id and a key
     * 
     * @param id
     * @param key
     */
    public Agent(int id, BigInteger key) {
        this.id = id;
        this.key = key;
    }

    // Getters
    public int getId() {
        return id;
    }

    public BigInteger getKey() {
        return key;
    }

    public String toString() {
        return String.format("Agent %d : %d", id, key.longValue());
    }
}
