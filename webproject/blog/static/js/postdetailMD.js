// 블로그 상세페이지의 목록태그를 시멘틱ui 태그로 바꿔주는 showdown 확장
showdown.extension('semantic', function() {
    return [
        {
            type: 'output',
            regex: /<li>([^]+?)<\/li>/gi,
            replace: function(s,match) {
                return '<li class="ui list">' + match + '</li>';
            }
        },
        {
            type: 'output',
            regex: /<ol>([^]+?)<\/ol>/gi,
            replace: function(s,match) {
                return '<ol class="ui list">' + match + '</ol>';
            }
        },
        {
            type: 'output',
            regex: /<ul>([^]+?)<\/ul>/gi,
            replace: function(s,match) {
                return '<ul class="ui list">' + match + '</ul>';
            }
        },
    ]
});
