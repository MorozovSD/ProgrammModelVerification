### funcSignature test
##function test_func_funcSignature() as bool(,,,,,)
##end function
##function test_func11() as stef
##end function
##function test_func11() as bool
##end function
#
## statement test
#function test_func_statement ()
##if a then
##        a = a;
##        a = a;
##    else
##        dim a as bool
##        dim a as bool
##end if
#
#
#dim a as bool (,,,)
#a + (-b / a) + -b and not a + -b or a + -b;
#if a + (-b / a) + -b and not a + -b or a + -b then
#    a7 = a8;
#else
#    if a6 then
#        a7 = a8;
#    end if
#end if
#
#if a then
#    a = 1;
#    if a1 then
#        a2 = a3;
#    end if
#    a4 = a5;
#else
#    if a6 then
#        a7 = a8;
#    end if
#end if
#
#while a11 > 0
#    #while a > 0
#     #   while a
#            a = a;
#            a = a;
#     #   wend
#    #wend
#wend
#do
#    do
#        do
#            dim a as bool
#        loop until b
#    loop until b
#loop until b
#
#break
#
#b = a + -b(1);
#b = a + -b;
#end function
#
#
##### expr test
#function test_func_expr()
#b = a + (-b / a) + -b and not a + -b or a + -b;
#b = test_func_statement(false) + test_func1111(false) + qqqq[false + 1];
#"fasffas";
#'f';
#false;
#test1(false, "fq1");
#end function
#
## simple
#function test_func_simple ()#
#if a then
#a = not a;
#else
#dim a as bool (,,,)
#end if
#end function
#
#
function test1()
#("dasd" + 324 + False)(false, "fq1");
# b = a - -b;
# test1(false, "fq1");
# test1.test2(false, "fq1");
get '1'.test2(get test1.test);
get '1'.((test2))(get test1.test);
#test2(false, "fq1");
end function
#
#function test2()
#test1(false, "fq1");
#end function

# class class_name
#     public a as bool
#     public function test1()
#         b = a - -b;
#     end function
#     declare function x1 lib math123
# end class

# sourceItem: {
#  |classDef: 'class' identifier member* 'end' 'class' {
#  member: modifier? (funcDef|field|externFuncDef);
#  field: list<identifier> ('as' typeRef)?;
#  modifier: 'public'|'private';
#  };
# };