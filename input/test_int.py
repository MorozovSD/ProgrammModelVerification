# declare function x lib math alias id
# declare function x2 lib math alias id2

function main()
dim b as bool
called_binary2(true, false);
("called"+"_binary")(1, 2);
called_binary(1, 2);
end function

function called_binary(a as int, b as int) as bool
dim a as int
a = 7;
while a > 5
    a = a - 1;
wend
print(a, b);
end function

function called_binary2(a as bool, b as bool) as bool
if false then
if true then
    dim a as bool
    a = false;
end if
else
dim a as string
    a = "test";
end if
# #

# # #
# # dim a as int
# # a = 7;
# # while a > 5
# #     while a > 5
# #         while a > 3
# #         a = a - 1;
# #     wend
# #     wend
# #
# # wend
# # #
# # dim a as int
# # a = 7;
# # do
# #    do
# #        do
# #             a = a - 1;
# #        loop until a > 5
# #    loop until a > 5
# # loop until a > 5
# #
# # dim a as int
# # a = 12;
# # do
# #     a = a - 1;
# #     if a < 6 then
# #         break
# #     end if
# # loop while a > 5
# # a = 12;
# # dim a,b as bool
# # a, b = true;
# # a and not b and true;
# # dim a,b as string
# # a, b = "1";
# # b = "2";
# # a + b + '3';
# # dim a,b as int
# # a, b = 1;
# # b = 2;
# # a + b + 3;
# # 'a' + 1;
# # 1 - -3 + 0x11;
# # 1 - -4 + 0x11;
called_binary(2, 3);
# # a[1] = 2 + 1;
# # a[1] = 100;
# # a[2] = 10;
# # b = 1 + a[1] + a[2];
end function