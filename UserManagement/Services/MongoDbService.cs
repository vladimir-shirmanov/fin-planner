using Microsoft.Extensions.Options;
using MongoDB.Driver;
using UserManagement.Models;

namespace UserManagement.Services;

public interface IMongoDbService
{
    Task<List<UserSettings>> GetAsync();
    Task<UserSettings?> GetAsync(string id);
    Task CreateAsync(UserSettings userSettings);
    Task UpdateAsync(string id, UserSettings userSettings);
    Task RemoveAsync(string id);
}

public class MongoDbService : IMongoDbService
{
    private readonly IMongoCollection<UserSettings> _userSettingsCollection;

    public MongoDbService(IOptions<MongoDbSettings> settings)
    {
        var client = new MongoClient(settings.Value.ConnectionString);
        var database = client.GetDatabase(settings.Value.DatabaseName);
        _userSettingsCollection = database.GetCollection<UserSettings>(settings.Value.CollectionName);
    }
    
    public async Task<List<UserSettings>> GetAsync() => await _userSettingsCollection.Find(_ => true).ToListAsync();
    public async Task<UserSettings?> GetAsync(string id) => await _userSettingsCollection.Find(u => u.UserId == id).FirstOrDefaultAsync();
    public async Task CreateAsync(UserSettings userSettings) => await _userSettingsCollection.InsertOneAsync(userSettings);
    public async Task UpdateAsync(string id, UserSettings userSettings) => await _userSettingsCollection.ReplaceOneAsync(u => u.Id == id, userSettings);
    public async Task RemoveAsync(string id) => await _userSettingsCollection.DeleteOneAsync(u => u.Id == id);
}