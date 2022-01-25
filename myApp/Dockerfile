FROM mcr.microsoft.com/dotnet/sdk:6.0

RUN mkdir /nuget-repo
COPY *.nupkg /nuget-repo
RUN dotnet nuget add source /nuget-repo --name local-repo

COPY create_and_run.sh /
CMD ["bash", "/create_and_run.sh"]
