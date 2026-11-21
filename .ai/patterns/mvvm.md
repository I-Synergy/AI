# Model-View-ViewModel (MVVM) Pattern

MVVM separates what the user sees (the View) from what the screen does (the ViewModel), and keeps the business rules in the Domains project behind the API. In this template the MVVM stack is the I-Synergy framework, used by the MAUI head (`{ApplicationName}.App`). The Blazor head (`{ApplicationName}.App.Web`) is plain Razor and does not use ViewModels; see "Blazor Head" below.

## Layers in a head

```mermaid
graph TB
    View[View<br/>XAML view, derives from View base]
    ViewModel[ViewModel<br/>ViewModelNavigation of TParam]
    Service[I-Synergy I{ApplicationName}ApiService<br/>in App.Shared]
    Api[Kiota client to the API]

    View -->|Data binding, commands| ViewModel
    ViewModel -->|Calls| Service
    Service -->|Maps generated models to Models| Api
```

- **View.** A XAML page. The root element is `c:View` (non-generic) and the code-behind passes the view model to the base constructor.
- **ViewModel.** Derives from `ViewModelNavigation<TParam>`, where `TParam` is the navigation parameter the page receives (`object` for a list, `Guid` for a detail page).
- **Service.** The head depends on `I{ApplicationName}ApiService` from `{ApplicationName}.App.Shared`. It never sees the Kiota types.

## Where each piece lives

| Piece | Project | Namespace |
|---|---|---|
| Views (`{Entities}View.xaml`, `{Entity}DetailView.xaml`, `ShellView.xaml`) | `{ApplicationName}.App` | `{ApplicationName}.Views` |
| ViewModels (`{Entities}ViewModel.cs`, `{Entity}DetailViewModel.cs`, `ShellViewModel.cs`) | `{ApplicationName}.App` | `{ApplicationName}.ViewModels` |
| Service abstraction and implementation | `{ApplicationName}.App.Shared` | `{ApplicationName}.Abstractions.Services`, `{ApplicationName}.Services` |
| Read models bound by the views | `{ApplicationName}.Models` | `{ApplicationName}.Models` |
| Startup, configuration, `Context` | `{ApplicationName}.App` | `{ApplicationName}` |

## ViewModel

Each ViewModel derives from `ViewModelNavigation<TParam>` from `ISynergy.Framework.Mvvm.ViewModels`. The base class supplies the common services, the navigation hooks, and the initialization state. The sample's list page:

```csharp
// File: {ApplicationName}.App/ViewModels/{Entities}ViewModel.cs
using System.Collections.ObjectModel;
using ISynergy.Framework.Core.Abstractions.Services;
using ISynergy.Framework.Mvvm.Abstractions.Services;
using ISynergy.Framework.Mvvm.Commands;
using ISynergy.Framework.Mvvm.ViewModels;
using Microsoft.Extensions.Logging;
using {ApplicationName}.Abstractions.Services;
using {ApplicationName}.Models;

namespace {ApplicationName}.ViewModels;

public class {Entities}ViewModel : ViewModelNavigation<object>
{
    private readonly I{ApplicationName}ApiService _apiService;
    private readonly INavigationService _navigationService;

    public {Entities}ViewModel(
        ICommonServices commonServices,
        ILogger<{Entities}ViewModel> logger,
        I{ApplicationName}ApiService apiService,
        INavigationService navigationService)
        : base(commonServices, logger)
    {
        _apiService = apiService;
        _navigationService = navigationService;

        Select{Entity}Command = new AsyncRelayCommand<{Entity}>((item, cancellationToken) => OpenDetailAsync(item, cancellationToken));
        RetryCommand = new AsyncRelayCommand(cancellationToken => LoadAsync(cancellationToken));
    }

    public override string Title => _commonServices.LanguageService.GetString("{Entities}");

    public ObservableCollection<{Entity}> Items { get; } = [];

    public bool IsLoading
    {
        get => GetValue<bool>();
        set => SetValue(value);
    }

    public string? ErrorMessage
    {
        get => GetValue<string?>();
        set
        {
            SetValue(value);
            RaisePropertyChanged(nameof(HasError));
        }
    }

    public new bool HasError => !string.IsNullOrEmpty(ErrorMessage);

    public AsyncRelayCommand<{Entity}> Select{Entity}Command { get; }

    public AsyncRelayCommand RetryCommand { get; }

    public override async Task InitializeAsync()
    {
        await base.InitializeAsync();

        if (!IsInitialized)
        {
            await LoadAsync();
            IsInitialized = true;
        }
    }

    private async Task LoadAsync(CancellationToken cancellationToken = default)
    {
        IsLoading = true;
        ErrorMessage = null;

        try
        {
            var items = await _apiService.Get{Entities}Async(cancellationToken);

            Items.Clear();
            foreach (var item in items)
                Items.Add(item);
        }
        catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
        {
            // Cancelled by the caller; nothing is shown.
        }
        catch (Exception)
        {
            ErrorMessage = _commonServices.LanguageService.GetString("Error_Placeholder");
        }
        finally
        {
            IsLoading = false;
        }
    }

    private async Task OpenDetailAsync({Entity}? item, CancellationToken cancellationToken = default)
    {
        if (item is null || cancellationToken.IsCancellationRequested)
            return;

        await _navigationService.NavigateAsync<{Entity}DetailViewModel>(item.{Entity}Id);
    }
}
```

Rules this follows:

- **Properties are framework bindings.** `GetValue<T>()` and `SetValue(value)` read and write the bindable store, so `[ObservableProperty]` (CommunityToolkit) is not used in the MAUI head.
- **Commands are `AsyncRelayCommand` from `ISynergy.Framework.Mvvm.Commands`**, constructed in the constructor. They receive a `CancellationToken`, which the command passes to the service.
- **Initialization runs once.** Override `InitializeAsync()`, call `base.InitializeAsync()`, and load only when `IsInitialized` is false. The framework signature has no cancellation token.
- **Errors are shown, not thrown.** A failed load sets `ErrorMessage`; the view shows it with a retry command. A cancellation the caller requested is not an error.
- **Navigation.** The view model asks `INavigationService` to open another view model with a typed parameter: `NavigateAsync<TViewModel>(parameter)`.
- **Titles and text come from resources.** `_commonServices.LanguageService.GetString(key)` reads the `{ApplicationName}.Resources` strings. Views use `{m:GetString Key}`.

A detail view model takes its identifier as the navigation parameter, `ViewModelNavigation<Guid>`, and reads it in `InitializeAsync()` from `Parameter`.

## View

A view is a XAML page whose root is the non-generic `c:View`. The code-behind passes the view model to the base class and does nothing else:

```csharp
// File: {ApplicationName}.App/Views/{Entities}View.xaml.cs
using {ApplicationName}.ViewModels;

namespace {ApplicationName}.Views;

public partial class {Entities}View
{
    public {Entities}View({Entities}ViewModel viewModel)
        : base(viewModel)
    {
        InitializeComponent();
    }
}
```

```xml
<!-- File: {ApplicationName}.App/Views/{Entities}View.xaml -->
<c:View
    xmlns:c="clr-namespace:ISynergy.Framework.UI.Controls;assembly=ISynergy.Framework.UI.Maui"
    xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
    xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
    xmlns:m="clr-namespace:ISynergy.Framework.UI.Markup;assembly=ISynergy.Framework.UI.Maui"
    xmlns:viewmodels="clr-namespace:{ApplicationName}.ViewModels"
    xmlns:models="clr-namespace:{ApplicationName}.Models;assembly={ApplicationName}.Models"
    x:Class="{ApplicationName}.Views.{Entities}View"
    x:DataType="viewmodels:{Entities}ViewModel">

    <CollectionView ItemsSource="{Binding Items}">
        <CollectionView.ItemTemplate>
            <DataTemplate x:DataType="models:{Entity}">
                <Label Text="{Binding Name}" />
            </DataTemplate>
        </CollectionView.ItemTemplate>
    </CollectionView>
</c:View>
```

- **No `x:TypeArguments`.** The root is not generic. The code-behind's base is supplied by the `View` alias in the project file, which resolves `ISynergy.Framework.UI.Controls.View`.
- **`x:DataType` is always set.** The project compiles bindings (`MauiXamlInflator=SourceGen`), so a binding without a data type fails to build.
- **Commands bind to the view model** (`Command="{Binding RetryCommand}"`).

## Shell

The shell is the one view that derives from `Shell` and implements `IShellView`. It hosts the tabs and binds the `ShellViewModel`, which derives from `BaseShellViewModel` and overrides the shell hooks. The shell view model is opened once the application is ready, from `App.OnApplicationLoaded`, with `_navigationService.NavigateModalAsync<ShellViewModel>()`.

The app does not set `MainPage`. Startup goes through the framework's `Application` overrides: `InitializeApplicationAsync()` runs the startup work and calls `SignalApplicationInitialized()`, and `OnApplicationLoaded` opens the shell.

## Commands in views

Views bind commands from the view model. There are no code-behind click handlers:

```xml
<Button Text="{m:GetString Retry}"
        Command="{Binding RetryCommand}"
        SemanticProperties.Hint="{m:GetString Retry}" />
```

`CollectionView.SelectionChangedCommand` binds the same way, with `SelectedItem` used to clear the selection after navigation.

## Dependency injection

The head's `MauiProgram.CreateMauiApp()` configures the framework, which discovers views and view models in the head's assembly by naming convention (`{X}View` with `{X}ViewModel`). Services are added in the `ConfigureServices` callback:

```csharp
builder
    .UseMauiAppForCurrentHead<App>()
    .ConfigureServices<App, Context, CommonServices, ExceptionHandlerService, SettingsService, global::{ApplicationName}.Resources.Properties.Resources>(
        appBuilder =>
        {
            appBuilder.Add{ApplicationName}ApiServices();
            appBuilder.Services.AddDeviceStore();
        },
        mainAssembly,
        assemblyName => assemblyName.Name!.StartsWith(typeof(App).Namespace!, StringComparison.Ordinal));
```

The six type arguments are the application, its context, the common services, the exception handler, the settings service, and the resource class. Do not add or drop one: the framework uses the positions.

Constructor-inject services into view models. Do not reach for `IPlatformApplication.Current.Services` from a view model; the one place the sample does this is `App.InitializeApplicationAsync`, where the startup has no constructor to inject into.

## Blazor head

The web head, `{ApplicationName}.App.Web`, is a plain Razor app on interactive server rendering. It does not use the I-Synergy MVVM stack, has no ViewModels, and does not derive from `View<TViewModel>`.

- Pages are `.razor` components under `Pages/`. A page injects `I{ApplicationName}ApiService` directly: `@inject I{ApplicationName}ApiService ApiService`.
- Form state is a private class inside the page, annotated with Data Annotations and bound with `EditForm`.
- Loading and error state are fields on the page, set in `OnInitializedAsync` and in the handlers. Cancel the work in `Dispose` through a `CancellationTokenSource`.
- Shared state across pages, when a page needs it, is a scoped class registered in the head's `ServiceCollectionExtensions`. The sample has none.

An optional component library (a UI kit of components) is added to the head's `_Imports.razor` and to `Routes.razor` or `MainLayout.razor`, and nowhere else. The sample uses no component library.

Correct and wrong, side by side:

```xml
<!-- Correct: the command is bound to the view model's AsyncRelayCommand -->
<Button Text="{m:GetString Retry}" Command="{Binding RetryCommand}" />

<!-- Wrong: a code-behind click handler bypasses the command, its cancellation token, and the test seam -->
<Button Text="Retry" Clicked="OnRetryClicked" />
```

## Testing ViewModels

ViewModels are tested through their public properties and commands, with the real service layer behind them. The API service is the only seam worth faking, because it is the network. Put the fake in the head's test project, implementing `I{ApplicationName}ApiService`, and assert on `Items`, `ErrorMessage`, and `IsLoading`:

```csharp
[TestMethod]
public async Task InitializeAsync_WhenTheApiFails_ShowsTheError()
{
    var viewModel = new {Entities}ViewModel(commonServices, NullLogger<{Entities}ViewModel>.Instance, new FailingApiService(), navigationService);

    await viewModel.InitializeAsync();

    Assert.IsNotNull(viewModel.ErrorMessage);
    Assert.IsEmpty(viewModel.Items);
}
```

Do not mock the framework's base classes. Do not use `Mock<INavigationService>` where a hand-written fake records the call; the choice is the test's, but a mock of a framework interface tends to break when the framework changes.

## Checklist

- [ ] The ViewModel derives from `ViewModelNavigation<TParam>` and calls `base(commonServices, logger)`
- [ ] Bindable properties use `GetValue<T>()` / `SetValue(value)`
- [ ] Commands are `AsyncRelayCommand` from `ISynergy.Framework.Mvvm.Commands`, built in the constructor, and receive a `CancellationToken`
- [ ] `InitializeAsync()` loads once and sets `IsInitialized`
- [ ] The view's root is `c:View` (non-generic) with `x:DataType` set, and the code-behind calls `base(viewModel)`
- [ ] Services are constructor-injected; the view model never reads `IPlatformApplication.Current`
- [ ] The Blazor head uses no ViewModels
