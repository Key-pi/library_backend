red=$(tput setaf 1)
green=$(tput setaf 2)
reset=$(tput sgr0)

# check docker
set -e
if docker -v; then
  echo "${green}Docker exists. ${reset}"
else
  echo "${red}Docker check failed. Please install docker ${reset}"+
fi

# check docker-compose
if docker-compose -v; then
  echo "${green}Docker Compose exists. ${reset}"
else
  echo "${red}Docker Compose check failed. Please install docker-compose ${reset}"+
fi

# generate .env file
if [ -f .env ]; then
  echo "${green}.env exists ${reset}";
else
  echo "${red}.env not found. ${green}Create a default .env file${reset}. ";
  cat example.env > .env
fi

echo "${green}Start building images... ${reset}"
docker-compose build
