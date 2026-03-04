#include <stdio.h>
#include <string.h>

// Program banner
void display_banner() {
    printf("=============================================\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠤⠴⠶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠂⠉⡇⠀⠀⠀⢰⣿⣿⣿⣿⣧⠀⠀⢀⣄⣀⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⢠⣶⣶⣷⠀⠀⠀⠸⠟⠁⠀⡇⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠘⠟⢹⣋⣀⡀⢀⣤⣶⣿⣿⣿⣿⣿⡿⠛⣠⣼⣿⡟⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⣴⣾⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣿⣿⠁⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠿⠇⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠳⣤⣙⠟⠛⢻⠿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣇⠘⠉⠀⢸⠀⢀⣠⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠈⠻⣷⣦⣼⠀⠀⠀⢻⣿⣿⠿⢿⡿⠿⣿⡄⠀⠀⣼⣷⣿⣿⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣶⣄⡈⠉⠀⠀⢸⡇⠀⠀⠉⠂⠀⣿⣿⣿⣧⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣷⣤⣀⣸⣧⣠⣤⣴⣶⣾⣿⣿⣿⡿⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠉⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    printf("=============================================\n\n");
    printf("<< Last message from the legendary anonymous hacker >>\n");
    printf("The legend says this program holds his final words...\n");
    printf("But only those who know the activation code can read them.\n\n");
}


// Function to check the activation code
int check_code(const char *input) {

    char correct_code[] = {
        0x06, 0x03, 0x09, 0x11, 0x0A, 0x0A, 0x39,
        0x0A, 0x73, 0x06, 0x06, 0x71, 0x0C,
        0x1D, 0x01, 0x72, 0x06, 0x71, 0x3F,
        0x00
    };

    for (int i = 0; correct_code[i] != '\0'; i++) {
        if (input[i] != (correct_code[i] ^ 0x42)) {
            return 0;
        }
    }

    // Ensure no extra characters
    if (input[strlen((char*)input)] != '\0') {
        return 0;
    }

    return 1;
}

int main() {

    char input[20] = {0};  // 19 chars + null terminator

    display_banner();

    printf("Enter the activation code: ");

    if (scanf("%19s", input) != 1) {
        printf("Input error.\n");
        return 1;
    }

    if (check_code(input)) {
        printf("\nAccess granted!\n");
        printf("Here are the final words of the legendary hacker:\n");
        printf("\"Sometimes, what you seek is hidden in the shadows...\"\n");
    } else {
        printf("\nIncorrect activation code. The secret remains concealed...\n");
    }

    return 0;
}
