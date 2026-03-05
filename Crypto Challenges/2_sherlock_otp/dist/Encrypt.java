import java.security.SecureRandom;

public class Encrypt {
    public static void main(String[] args) {
        System.out.println("\n");
        System.out.println("  ____  _               _            _    ");
        System.out.println(" / ___|| |__   ___ _ __| | ___   ___| | __");
        System.out.println(" \\___ \\| '_ \\ / _ \\ '__| |/ _ \\ / __| |/ /");
        System.out.println("  ___) | | | |  __/ |  | | (_) | (__|   < ");
        System.out.println(" |____/|_| |_|\\___|_|  |_|\\___/ \\___|_|\\_\\");
        System.out.println("       SHERLOCK'S CRYPTO LAB\n");

        SecureRandom random = new SecureRandom();
        // The "Secure" One Time Pad
        // Generating pad ONCE, but it's used multiple times!
        byte[] key = new byte[60];
        random.nextBytes(key); 

        String[] messages = {
            "Watson, I have found the location of the stolen diamonds.     ",
            "Moriarty's men are unaware. We move at the strike of midnight.",
            "REDACTED                                                      "
        };

        for (int i = 0; i < messages.length; i++) {
            byte[] msgBytes = messages[i].getBytes();
            byte[] encrypted = new byte[msgBytes.length];
            for (int j = 0; j < msgBytes.length; j++) {
                encrypted[j] = (byte) (msgBytes[j] ^ key[j]);
            }
            
            System.out.print("Broadcast " + (i + 1) + ": ");
            for (byte b : encrypted) {
                System.out.printf("%02x", b);
            }
            System.out.println();
        }
    }
}
