from BlueDawn import main

if __name__ == "__main__":
    ans = main()
    with open("result.txt", "w") as f:
        f.write(str(ans))
    print(ans)