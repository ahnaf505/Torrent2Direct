#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool isValidMagnetLink(const char *link) {
    if (strncmp(link, "magnet:?", 8) != 0) {
        return false;
    }
    if (strstr(link, "xt=urn:btih:") == NULL) {
        return false;
    }
    return true;
}

int main() {
    char magnetLink[2048];

    printf("Enter a magnet link: ");
    if (fgets(magnetLink, sizeof(magnetLink), stdin) != NULL) {
        magnetLink[strcspn(magnetLink, "\n")] = '\0';
        if (isValidMagnetLink(magnetLink)) {
            printf("Checking torrent metadata...");
        } else {
            printf("Invalid magnet link. Please try again.\n");
            return 1;
        }
    } else {
        printf("Failed to read the magnet link.\n");
    }

    return 0;
}
