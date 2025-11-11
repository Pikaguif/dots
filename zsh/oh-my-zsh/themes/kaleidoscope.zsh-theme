if [[ $(tput colors) -ge 256 ]]; then
    black="%F{0}"
    red="%F{160}"
    orange="%F{166}"
    yellow="%F{220}"
    purple="%F{99}"
    gray="%F{252}"
    white="%F{15}"
else
    black="%F{black}"
	red="%F{red}"
    orange="%F{yellow}"
	yellow="%F{white}"
    purple="%F{magenta}"
    gray="%F{white}"
    white="%F{white}"
fi 

if [[ $(tput colors) -ge 256 ]]; then
    bg_black="%K{0}"
    bg_red="%K{160}"
    bg_orange="%K{166}"
    bg_yellow="%K{220}"
    bg_purple="%K{99}"
    bg_gray="%K{252}"
    bg_white="%K{15}"
else
	bg_black="%K{black}"
	bg_red="%K{red}"
    bg_orange="%K{yellow}"
	bg_yellow="%K{white}"
    bg_purple="%K{magenta}"
    bg_gray="%K{gray}"
    bg_white="%K{white}"
fi 

#${gray}➩ $B${black}🭮

PROMPT="${bg_black}${white}  %(?:✔ :✖ )  ${purple}🭨${white}${bg_purple}     ${red}🭨${white}${bg_red} %* ${orange}🭨${white}${bg_orange} %D ${yellow}🭨${black}${bg_yellow} %3~ ${yellow}%k🭬
${bg_white}${black}  $   ${white}%k🭬 %b${gray}"
POSTEDIT="$(tput sgr0)"
