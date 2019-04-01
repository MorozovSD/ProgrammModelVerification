declare function MessageBoxW(handleKind as int, Title as string, Message as string, SomeThing as int) as int lib user32

function main()
dim a as bool(,,)
a(0) = true;
a(1) = a(0);
a(2) = a(0);
# a(0) = a(1) and a(1);
MessageBoxW(0, "test1", "test2", 1);
main2();
main2();
main2();
#
main1("test1", "test111");
#
main1("test111", "test1167567");
end function


function main1(handleKind as string, something as string)
MessageBoxW(0, handleKind, something, 1);
end function

function main2()
MessageBoxW(0, "test1", "test2", 1);
end function



#
# class String
#     public buff as char()
#     public length, capacity as int
#
    # public function String(str as string, l as int)
        # this.capac/ity = (l + 1) * 2;
        # this.length = l;
        # this.buff = char(capacity);

        # dim i as int
        # while i < l
            # buff(i) = str(i);
            # i = i + 1;
        # wend

    # end function
#
    # public function Add(ch as char)
    #     dim nl as int
        # nl = this.length + 1
        # if (nl >= this.capacity) then
        #     this.capacity = this.capacity * 2;
            # dim t as char()
            # t = char(capacity);

            # dim i as int
            # i = 0;
            # while i < this.length
            #     t(i) = buff(i);
            #     i = i + 1;
            # wend

            # this.buff = t;
        # end if

        # this.buff(length) = ch;
        # this.length = this.length + 1;
    # end function
#
#     public function Add(str as string, l as int)
#
#     end function
#
#     public function Add(str as String)
#
#     end function
#
# end class
#
# class Console
#     declare function GetStdHandle(handleKind as int) as int lib kernel32
#     declare function SetConsoleMode(handle as int, mode as int) as int lib kernel32
#     declare function ReadFile(handle as int, buff as char(), count as int, taken as int(), reserved as int) as int lib kernel32
#     declare function WriteFile(handle as int, buff as char(), count as int, taken as int(), reserved as int) as int lib kernel32
#
#     private hIn, hOut as int
#
#     function Console()
#         hIn = GetStdHandle(-11);
#         SetConsoleMode(hId, 0);
#         // hOut = ...
#     end function
#
#     public function Write(s as String)
#
#     end function
#
#     public function WriteLine(s as String)
#
#     end function
#
#     public function ReadLine() as String
#
#     end function
#
# end class
#
#
#
# declare function MessageBoxW(handleKind as int, Title as string, Message as string, SomeThing as int) as int lib user32

# function main()
# ctypes.c_int, ctypes.c_int, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_int

# MessageBoxW(1, "HELLO WORLD", "Something New", 0);
# dim con as Console
# con = Console();
# con.Write(String("Enter your name: ", 17));

# dim name as String
# name = con.ReadLine();

# dim msg as String
# msg = String("hello ", 6);
# msg.Add(name);
# msg.Add("!", 1);

# con.WriteLine(msg);

# con.ReadLine();

# end function
