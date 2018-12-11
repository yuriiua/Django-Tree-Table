
    function getBossName(allData, bossId) {
    for(var i = 0; i < allData.length; i++){
        if(allData[i]['id'] == bossId){
            return allData[i]['fullName']
        }
    }
    }

    function tableBuild2(allData) {
    var checkLevel = {
        '1':true,
        '2':false,
        '3':false,
        '4':false,
        '5':false};
    var listLevel = [1,2,3,4,5];

    for(var i=0; listLevel[i] <= 5 ; i++) {

        $.each(allData, function (itemid) {

            var data = allData[itemid];
            var level = parseInt(data['level']);
            checkLevel[level] = true;


            //chek if row exist
            if (!$("#" + data['id']).length && level == listLevel[i]) {


                //create row
                var $tr = $('<tr id="' + data['id'].toString() + '" ></tr>');
                //row attr and class
                $tr.attr('level', level).addClass('collapsed level' + level);
                $tr.attr('bossID', data['bossID']);
                //add parent attr
                if (level > 1) {
                    ($("#" + data['bossID']).hasClass('expanded')) ? $tr.attr('style', '') : $tr.attr('style', 'display:none');
                    $tr.attr('data-tt-id', $("#" + data['bossID']).attr('data-tt-id') + "-" + data['id']);
                    $tr.attr("data-tt-parent-id", $("#" + data['bossID']).attr('data-tt-id'));
                } else {
                    $tr.attr('data-tt-id', data['id']);
                }
                //add indenter and row class by level
                var $td_indenter = $('<td></td>');
                if (level == 5) {
                    $tr.addClass('leaf');
                    $td_indenter.append('<span></span>');
                } else {
                    $tr.addClass('branch');
                    $td_indenter.append('<span class="indenter" style="padding-left: 0px;"><a class="expander" href="#" title="Expand">&nbsp;</a></span>');
                }

                var $td_position = $('<td></td>').addClass('position').html(data['position']);
                var $td_fullName = $('<td></td>').addClass('fullName').html(data['fullName']);
                var $td_bossName = $('<td></td>').addClass('bossName').html(data['bossName']);
                var $td_salary = $('<td></td>').addClass('salary').html(data['salary']);
                var $td_employed = $('<td></td>').addClass('employeeDate').html(data['employeeDate']);
                var $td_detail = $('<td class="detail"><a href="detailPage?ID=' + data['id'] + '">detail</a></td>');
                $tr.append($td_indenter, $td_position, $td_fullName, $td_bossName, $td_salary, $td_employed, $td_detail)

                var $bossRow = $('#' + data['bossID'])
                if ($bossRow.length > 0) {
                    $bossRow.after($tr);
                } else {
                    $('tbody').append($tr);
                }


            }
        });
        //check if level in list exist
        for(var z = 1; z <=5; z++){
            if(!checkLevel[z]){

                if(listLevel.indexOf(z)>=0){
                    listLevel.splice(listLevel.indexOf(z),1)
                }

            }
        }
    }
    }

    function LazzyTableLoadBy(bossid, sortBy) {
    $("#loaderBox").css('display', 'block');
    $.getJSON('/jsonTableByID',{bossID:bossid,order_by:sortBy}).done(function (data) {
        tableBuild2(data.table);
        //$.each(data.table, function (item) {tableBuildLazy(data.table,data.table[item])});

        $("#loaderBox").css('display', 'none')
    });
    }

    function parents(ttid) {

        $('[data-tt-parent-id]').each(function () {
            if ($(this).attr('data-tt-parent-id').indexOf(ttid) >=0){
                $(this).css('display', 'none').removeClass('expanded').addClass('collapsed');
            }
        })

    }

    function treeTable(cmd) {
        if(cmd == 'expandAll'){
            $('[data-tt-id]').attr('style', '').removeClass('collapsed').addClass('expanded');
        }else{
            $('[data-tt-id]').removeClass('expanded').addClass('collapsed');
            $('[data-tt-id]').not('#1').attr('style', 'display:none');
        }
    }

    function searchByForm() {

    var searcher = document.forms.searcher;
    var options = {};
    var keyName = searcher.elements.searchBy.value;
    var searchValue = searcher.elements.inputTerm.value;

    if(searchValue==''){
        return
    }
    if (keyName=='bossID'){

        options[keyName] = $( "tr:contains("+searchValue+")" ).prop('id');
    }else{
        options[keyName] = searchValue;
    }


    $.getJSON('/searchBy', options).done(function (data) {

        $('[data-tt-id]').attr('style', 'display:none');

        tableBuild2(data.table);
        for (var i=0; i< data.table.length; i++){
            $("#"+data.table[i]['id']).css("display", '').removeClass('collapsed').addClass('expanded')
        }
    }

        )

    }

    function toggleClass(thisClass) {
        var filterElement = $('.'+thisClass);
        var type = ['alpha','alpha','alpha','alpha','number', 'date'];
        var searchField = $('.'+thisClass).prop('id').split('_')[1];
        var typeId = thisClass.split('_')[1];
        $('.sorter').not('.'+thisClass).removeClass('up down').html('');
            if (filterElement.hasClass('down')) {
                filterElement.html('').html('&#x25B2;').removeClass('down').addClass('up');
            } else if (filterElement.hasClass('up')) {
                filterElement.html('').html('&#x25BC;').removeClass('up').addClass('down');
            }else{
                filterElement.html('&#x25BC;').addClass('down');
        }

        if(filterElement.hasClass('down','up')){

            sortElements(searchField, 'down', type[typeId] )
        }else{

            sortElements(searchField, 'up', type[typeId] )
        }


    }

    function sortData(key, data, type, direct) {


        // sort by value
        if(type == 'number'){
            if(direct == 'down'){
                data.sort(function (a, b) {return parseInt(a[key]) - parseInt(b[key])});
            }else{
                data.sort(function (a, b) {return parseInt(b[key]) - parseInt(a[key])});
            }

        }else if (type == 'alpha') {
            if(direct == 'up'){

                data.sort(function(a, b) {
                    var nameA = a[key].toUpperCase(); // ignore upper and lowercase
                    var nameB = b[key].toUpperCase(); // ignore upper and lowercase
                    if (nameA < nameB) {return -1}
                    if (nameA > nameB) {return 1}
                });
            }else{

                data.sort(function(a, b) {
                    var nameA = a[key].toUpperCase(); // ignore upper and lowercase
                    var nameB = b[key].toUpperCase(); // ignore upper and lowercase
                    if (nameA > nameB) {return -1}
                    if (nameA < nameB) {return 1}
                });
            }

        }else if(type == 'date'){
            if(direct == 'up'){
                data.sort(function(a, b) {
                    var nameA = Date.parse(a[key]); //
                    var nameB = Date.parse(b[key]); //
                    if (nameA > nameB) {return -1}
                    if (nameA < nameB) {return 1}
                });
            }else{
                data.sort(function(a, b) {
                    var nameA = Date.parse(a[key]); //
                    var nameB = Date.parse(b[key]); //
                    if (nameA < nameB) {return -1}
                    if (nameA > nameB) {return 1}
                });
            }
        }
        return data
    }

    function sortElements(field, direction, type) {
        var ElementList = $('[data-tt-id]');
        var sortedElements = {};
        var sortList = [];
        var toSort = ElementList.length;

        for (var i=0; i < toSort; i++) {
            var $elmnt = $('#' + ElementList[i].id);
            var elmId = ElementList[i].id;

            sortList.push({
                bossID: $elmnt.attr('bossID'),
                employeeDate: $elmnt.children('.employeeDate').text(),
                fullName: $elmnt.children('.fullName').text(),
                id: parseInt(elmId),
                level: parseInt($elmnt.attr('level')),
                position: $elmnt.children('.position').text(),
                salary: parseInt($elmnt.children('.salary').text()),
                bossName:$elmnt.children('.bossName').text()
            });

        }
        var sorted = sortData(field, sortList, type, direction);


        ElementList.remove();
        tableBuild2(sorted);


    return
    }

    $(document).ready(function () {
        document.getElementById("searchForm").addEventListener("click", function(event){
    event.preventDefault()
    });



        $("#employeeTable").on("mousedown", ".expander", function() {
        var parentId = $(this).closest('tr').attr('data-tt-id');
        var level = $(this).closest('tr').attr('level');
        var selectorId = '[data-tt-parent-id="'+parentId+'"]';
        var thisid = $(this).closest('tr').prop('id');
        var childLength = $(selectorId).length;



    if(level == 4 && childLength < 1){

        var sortBy = ($('.up,.down').length > 0)? $('.up,.down').attr('id').split('_')[1]:'';
        var direction = ($('.up,.down').hasClass('up'))?'-':'';
        LazzyTableLoadBy(thisid,direction+sortBy)
    }

    $(this).closest('tr').toggleClass("expanded");
    $(this).closest('tr').toggleClass("collapsed");

    if($(this).closest('tr').hasClass('expanded')){
        $(selectorId).attr('style','');
    }else{
        parents(parentId);
    }

    });

        $('#searchForm').on('change', '.search_selector', function () {

            var type = $(this).val();

            var types = {
                'position':'text',
                'fullName':'text',
                'salary_less':'number',
                'salary_more':'number',
                'bossName':'text',
                'employed_before':'date',
                'employed_after':'date'
            };

            $("#searchInput").attr('type', types[type]);

            });


        $.getJSON('/jsonTableAll').done(function (data) {
         tableBuild2(data.table);

        //$.each(data.table, function (item) {tableBuild(data.table,data.table[item])});

        });
    });







