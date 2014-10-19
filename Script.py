script = '''
    function DoSubmit(str){
        var elem = document.getElementById('myForm').elements;
        for(var i = 0; i < elem.length; i++) 
            if(elem[i].name != "submit" && elem[i].name != "")    
                elem[i].value = Escape(elem[i].value);
    
        myForm.submit();
        return true;
    };

    function Escape (str) {
        return str.replace(/[\\0\\n\\r"'\\\\\\%]/g, function (char) {
            switch (char) {
                case "\\0":
                    return "\\\\0";
                case "\\n":
                    return "\\\\n";
                case "\\r":
                    return "\\\\r";
                case "\\\"":
                case "\'":
                case "\\\\":
                case "%":
                    return "\\\\"+char;
            }
       });
    };

'''