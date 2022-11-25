function()
    local t1 = {1,2,3,4,5,6,7,8,0}
    local t2 = {1,2,3,4,5,6,7,7,0}
    for i = 1, #t2 do
        t1[#t1 + 1] = t2[i]
    end
    return t1
end