using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace UserManagement.Models;

public class UserSettings
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }

    [BsonElement("user_id")] public string UserId { get; set; } = null!;

    [BsonElement("photo_url")] public string? PhotoUrl { get; set; }

    [BsonElement("main_currency")] public string MainCurrency { get; set; } = "USD";
}