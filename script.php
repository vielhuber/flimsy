<?php
$data = [
    "cfix" => "clear:both;\ndisplay:table;\ncontent:\"\"",
    "gitu %a" => "git add -A . && git commit -m %a && git push origin master",
    "gitr %a %b" => "git add -A . && git commit -m %a && git push origin master && git tag -a %b -m %a && git push --tags",
    "npm %a %b" => "npm --no-git-tag-version version %b && npm publish && git add -A . && git commit -m %a && git push origin master && git tag -a %b -m %a && git push --tags",
];

$command = 'dkhgfjlwbvgedhg wekjhgkgdskjhgdskfjghksdkjsdhg fkjdg jgksd kfjhg gitu this is a fucking test';
$command = 'dkhgfjlwbvgedhg wekjhgkgdskjhgdskfjghksdkjsdhg fkjdg jgksd kfjhg gitr "this is a fucking test" "foo"';

foreach($data as $data__key=>$data__value)
{
    
    $identifier = explode(' ',$data__key)[0];
    $pos = strrpos($command, $identifier);
    $cur = $pos;
    $source = explode(' ',$data__key);
    $target = [''];
    $inside_quotes = false;
    $placeholder = [];
    $replace = true;
    $final_command = $data__value;

    if( $pos === false )
    {
        continue;
    }

    while($cur < strlen($command))
    {
        $char = substr($command,$cur,1);
        $cur++;
        if( $char === '"' )
        {
            $inside_quotes = !$inside_quotes;
        }
        if( $char === ' ' && $inside_quotes === false )
        {
            $target[] = '';
            continue;
        }  
        $target[count($target)-1] .= $char;
    }

    // special case: one is allowed to omit quotes when only one placeholder is available
    if( count($source) !== count($target) && count($source) === 2 && $source[1] === '%a' )
    {
        $new_target = [];
        $new_target[0] = $target[0];
        unset($target[0]);
        $new_target[1] = '"'.implode(' ',$target).'"';
        $target = $new_target;
    }

    if( count($source) !== count($target) )
    {
        continue;
    }

    foreach($source as $source__key=>$source__value)
    {
        if( strpos($source__value, '%') === 0 )
        {
            $placeholder[$source__value] = $target[$source__key];
        }   
        else if( $source[$source__key] !== $target[$source__key] )
        {
            $replace = false;
            break;
        }
    }

    if( $replace === false )
    {
        continue;
    }
    
    foreach($placeholder as $placeholder__key=>$placeholder__value)
    {
        $final_command = str_replace($placeholder__key, $placeholder__value, $final_command);
    }

    print_r($final_command);

}