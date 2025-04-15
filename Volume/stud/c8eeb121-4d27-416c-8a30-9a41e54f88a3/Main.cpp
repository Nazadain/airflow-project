#include <iostream>

int main()
{
    int n;
    std::cin >> n;

    if (n > 1)
    {
        int a = 0, b = 1;
        for (int i = 2; i <= n; i++)
        {
            int c = a + b;
            a = b, b = c;
        }
        std::cout << b;
    }
    else std::cout << n;
    return 0;
}