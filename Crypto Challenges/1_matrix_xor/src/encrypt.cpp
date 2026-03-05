#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

using namespace std;

void print_banner() {
    cout << "\n";
    cout << "  /  | __ *| |* _ __(*)*  __\n";
    cout << " | |/| |/ *` | **| '**| \\ / /\n";
    cout << " | |  | | (*| | |*| |  | |>  <\n";
    cout << " |*|  |*|_*,*|_*|*|  |*/_/_\n";
    cout << "   MATRIX ACCESS NODE\n\n";
}

string xor_encrypt(const string& message, char key) {
    string result = message;
    for (size_t i = 0; i < message.length(); ++i) {
        result[i] = message[i] ^ key;
    }
    return result;
}

int main() {
    print_banner();
    
    // The red pill
    string flag = "DAKSHH{n30_f0und_th3_r3d_p1ll_x0r}";
    char key = 42; 
    
    string encrypted = xor_encrypt(flag, key);
    
    cout << "Encrypted Transmission:\n";
    for (size_t i = 0; i < encrypted.length(); ++i) {
        cout << hex << setfill('0') << setw(2) << (int)(unsigned char)encrypted[i];
    }
    cout << endl;
    
    return 0;
}
