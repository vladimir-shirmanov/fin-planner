FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
RUN apt-get -y update && apt-get -y install curl
USER $APP_UID
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["UserManagement.csproj", "./"]
RUN dotnet restore "UserManagement.csproj"
COPY . .
WORKDIR "/src/"
RUN dotnet build "UserManagement.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "UserManagement.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "UserManagement.dll"]
