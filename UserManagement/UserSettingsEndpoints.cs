using System.Security.Claims;
using Microsoft.AspNetCore.Mvc;
using UserManagement.Models;
using UserManagement.Services;

namespace UserManagement;

public static class UserSettingsEndpoints
{
    public static void MapUserSettingsEndpoints(this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/settings").RequireAuthorization(); // Require authentication for all endpoints

        group.MapGet("/", GetUserSettings)
            .WithName("GetUserSettings")
            .Produces<UserSettings>(StatusCodes.Status200OK)
            .Produces(StatusCodes.Status404NotFound)
            .WithTags("User Settings");

        group.MapPost("/", CreateOrUpdateUserSettings)
            .WithName("CreateOrUpdateUserSettings")
            .Accepts<UserSettings>("application/json")
            .Produces(StatusCodes.Status201Created)
            .WithTags("User Settings");
    }

    private static async Task<IResult> GetUserSettings(
        ClaimsPrincipal user,
        IMongoDbService db,
        [FromServices] ILogger logger)
    {
        // Extract userId from JWT claims
        var userId = user.FindFirst(ClaimTypes.NameIdentifier)?.Value;

        if (string.IsNullOrEmpty(userId))
        {
            logger.LogWarning("Unauthorized access attempt");
            return Results.Unauthorized();
        }

        logger.LogInformation("Fetching user settings for user {UserId}", userId);

        var settings = await db.GetAsync(userId);
        return settings is not null ? Results.Ok(settings) : Results.NotFound();
    }

    private static async Task<IResult> CreateOrUpdateUserSettings(
        UserSettings user, 
        ClaimsPrincipal claimsPrincipal, 
        IMongoDbService db, 
        [FromServices] ILogger logger)
    {
        var userId = claimsPrincipal.FindFirst(ClaimTypes.NameIdentifier)?.Value;

        if (string.IsNullOrEmpty(userId))
        {
            logger.LogWarning("Unauthorized access attempt");
            return Results.Unauthorized();
        }

        logger.LogInformation("Creating or updating settings for user {UserId}", userId);

        try
        {
            // Set the userId from the token into the UserSettings object
            user.UserId = userId;

            var existingUser = await db.GetAsync(user.UserId);
            if (existingUser is not null)
            {
                await db.UpdateAsync(existingUser.Id!, user);
                logger.LogInformation("Successfully updated settings for user {UserId}", user.UserId);
                return Results.NoContent();
            }

            await db.CreateAsync(user);
            logger.LogInformation("Successfully created settings for user {UserId}", user.UserId);
            return Results.Created($"/settings/{user.UserId}", user);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "An error occurred while creating or updating settings for user {UserId}", user.UserId);
            return Results.Problem("An error occurred while processing your request.");
        }
    }
}